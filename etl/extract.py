from collections.abc import Iterator
from api.client import HHClient
from models.hh import HHVacancy
from utils.logger import logger

class VacancyExtractor:
    def __init__(self, client: HHClient) -> None:
        self._client = client

    def extract(self) -> Iterator[HHVacancy]:
        page = 0
        while True:
            response = self._client.get_vacancies(page)

            logger.info(
                f"Processing page {page + 1}/{response['pages']}"
            )

            yield from response["items"]
            if page >= response["pages"] - 1:
                break
            page += 1
