import logging
import httpx
import re
import time
from config import settings
from exceptions.api import HHAPIError
from models.search import SearchRequest
from models.hh import HHVacancyPage

logger = logging.getLogger(__name__)

class HHClient:
    def __init__(self) -> None:
        self._client = httpx.Client(
            base_url=settings.hh_base_url,
            timeout=settings.request_timeout,
            headers={
                "User-Agent": settings.user_agent,
            },
        )
        self._static_version: str | None = None
        self._request_count = 0

    def __enter__(self) -> "HHClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    def _get_response(self, url: str, **kwargs) -> httpx.Response:
        try:
            response = self._client.get(url, **kwargs)
            response.raise_for_status()
            return response

        except httpx.HTTPStatusError as exc:
            raise HHAPIError(
                f"GET {url} failed\n"
                f"Status: {exc.response.status_code}\n"
                f"Headers: {dict(exc.response.headers)}\n"
                f"Body: {exc.response.text[:200]}",
                response=exc.response,
            ) from exc

        except httpx.HTTPError as exc:
            raise HHAPIError(f"GET {url} failed: {exc}") from exc

    def _get(self, url: str, accept: str, **kwargs) -> httpx.Response:
        headers = kwargs.pop("headers", {})
        return self._get_response(
            url,
            headers={
                **headers,
                "Accept": accept,
            },
            **kwargs,
        )

    def _get_json(self, url: str, **kwargs) -> dict:
        return self._get(url, "application/json", **kwargs).json()

    def _get_html(self, url: str, **kwargs) -> str:
        return self._get(url, "text/html", **kwargs).text

    @staticmethod
    def _extract_static_version(html: str) -> str:
        match = re.search(r'"build":\s*"([^"]+)"', html)
        if match is None:
            raise HHAPIError(
                f"Could not determine HH build version. "
                f"Response begins with: {html[:120]!r}"
            )
        return match.group(1)

    def _set_static_version(self, version: str) -> None:
        self._static_version = version
        self._client.headers.update({
            "Accept": "application/json",
            "X-Static-Version": version,
        })

    def _bootstrap_once(self) -> None:
        html = self._get_html(settings.hh_search_path)
        version = self._extract_static_version(html)
        self._set_static_version(version)
        logger.info("Using X-Static-Version %s", version)

    def _bootstrap(self) -> None:
        for attempt in range(3):
            try:
                self._bootstrap_once()
                return
            except HHAPIError as exc:
                logger.warning(
                    "Bootstrap attempt %s failed: %s",
                    attempt + 1,
                    exc,
                )
                time.sleep(2)
        raise HHAPIError("Bootstrap failed after retries")

    def _ensure_bootstrapped(self) -> None:
        if self._static_version is None:
            self._bootstrap()

    def _request_json(self, url: str, **kwargs) -> dict:
        self._request_count += 1
        exc_last: HHAPIError | None = None
        seen_versions: set[str] = set()
        for attempt in range(10):
            try:
                return self._get_json(url, **kwargs)
            except HHAPIError as exc:
                if (exc.response is None
                or exc.response.status_code != 406):
                    raise
                exc_last = exc
                seen_versions.add(self._static_version)
                logger.warning(
                    "406 attempt=%d server=%s x-static-version=%s x-request-id=%s",
                    attempt + 1,
                    exc.response.headers.get("server"),
                    self._static_version,
                    exc.response.headers.get("x-request-id"),
                )
                old_version = self._static_version
                self._bootstrap()
                seen_versions.add(self._static_version)
                if self._static_version != old_version:
                    logger.warning(
                        "X-Static-Version %s -> %s",
                        old_version,
                        self._static_version,
                    )
                time.sleep(min(2 ** attempt, 10))
        raise HHAPIError(
            "Failed after bootstrap retries. "
            f"Observed versions: {sorted(seen_versions)}",
            response=exc_last.response,
        ) from exc_last

    def get_vacancies(self, request: SearchRequest, page: int) -> HHVacancyPage:
        self._ensure_bootstrapped()
        response = self._request_json(
            settings.hh_search_path,
            params=request.params | {"page": page},
        )
        search_result = response["vacancySearchResult"]
        paging = search_result.get("paging")
        next_block = paging.get("next") if paging else None
        return {
            "page": page,
            "next_page": (next_block["page"]
                if next_block and not next_block["disabled"]
                else None
            ),
            "vacancies": search_result["vacancies"],
            "found": search_result["totalResults"],
            "search_clusters": response["searchClusters"],
        }

if __name__ == '__main__':
    import json
    client = HHClient()
    data = client._request_json(settings.hh_search_path, params={"page": 0})
    with open("hh_vacancy_page.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
