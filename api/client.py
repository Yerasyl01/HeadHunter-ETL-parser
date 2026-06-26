import httpx
from config import settings
from exceptions.api import HHAPIError
from models.hh import HHVacancyResponse

class HHClient:
    def __init__(self) -> None:
        self._client = httpx.Client(
            base_url=settings.hh_base_url,
            timeout=settings.request_timeout,
            headers={
                "User-Agent": settings.user_agent,
            },
        )

    def __enter__(self) -> "HHClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    def _get(self, url: str, **kwargs) -> dict:
        try:
            response = self._client.get(url, **kwargs)
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as exc:
            raise HHAPIError(
                f"GET {url} failed: "
                f"{response.status_code} {response.text}"
            ) from exc

    def get_vacancies(self, page: int) -> HHVacancyResponse:
        return self._get(
            "/vacancies",
            params={
                "host": settings.hh_host,
                "page": page,
                "per_page": settings.per_page,
            },
        )
