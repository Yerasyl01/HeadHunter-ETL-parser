from api.client import HHClient
from contracts import VacancyQueue
from utils.logger import logger

class VacancyProducer:
    def __init__(self, client: HHClient, queue: VacancyQueue) -> None:
        self._client = client
        self._queue = queue

    def run(self) -> int:
        page = 0
        queued = 0
        while True:
            response = self._client.get_vacancies(page)
            logger.info(f"Processing page {page + 1}")
            for vacancy in response["vacancies"]:
                self._queue.push(vacancy)
                queued += 1
            if not response["has_next"]:
                break
            page += 1
        return queued
