import httpx
import re
from config import settings
from exceptions.api import HHAPIError
from models.hh import HHVacancyPage
from utils.logger import logger

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
                status_code=exc.response.status_code
            ) from exc

        except httpx.HTTPError as exc:
            raise HHAPIError(f"GET {url} failed: {exc}") from exc

    def _get_json(self, url: str, **kwargs) -> dict:
        return self._get_response(url, **kwargs).json()

    def _get_html(self, url: str, **kwargs) -> str:
        return self._get_response(url, **kwargs).text

    @staticmethod
    def _extract_static_version(html: str) -> str:
        match = re.search(r'build:\s*"([^"]+)"', html)
        if match is None:
            raise HHAPIError("Could not determine HH build version.")
        return match.group(1)

    def _bootstrap(self) -> None:
        html = self._get_html(settings.hh_search_path)
        self._static_version = self._extract_static_version(html)
        logger.info(f"Using X-Static-Version {self._static_version}")
        self._client.headers.update({
            "Accept": "application/json",
            "X-Static-Version": self._static_version,
        })

    def _ensure_bootstrapped(self) -> None:
        if self._static_version is None:
            self._bootstrap()

    def get_vacancies(self, page: int) -> HHVacancyPage:
        self._ensure_bootstrapped()

        try:
            response = self._get_json(
                settings.hh_search_path,
                params={"page": page},
            )

        except HHAPIError as exc:
            if exc.status_code != 406:
                raise
            logger.warning("Received 406. Refreshing static version and retrying...")
            self._bootstrap()
            response = self._get_json(
                settings.hh_search_path,
                params={"page": page},
            )

        search_result = response["vacancySearchResult"]
        paging = search_result["paging"]

        return {
            "page": page,
            "has_next": not paging["next"]["disabled"],
            "vacancies": search_result["vacancies"],
        }
