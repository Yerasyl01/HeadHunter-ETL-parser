import logging
from api.hh_client import HHClient
from contracts import VacancyQueue
from models.search import SearchRequest
from producer.search_planner import SearchPlanner

logger = logging.getLogger(__name__)

class VacancyProducer:
    def __init__(
        self,
        client: HHClient,
        queue: VacancyQueue,
        planner: SearchPlanner,
    ) -> None:
        self._client = client
        self._queue = queue
        self._planner = planner

    def _produce_request(self, request: SearchRequest) -> int:
        page = 0
        queued_for_request = 0
        while True:
            response = self._client.get_vacancies(request, page)
            vacancies = response["vacancies"]
            next_page = response["next_page"]
            logger.info(
                "Page %d: %d vacancies, next=%r",
                page + 1,
                len(vacancies),
                next_page,
            )
            for vacancy in vacancies:
                self._queue.push(vacancy)
                queued_for_request += 1
            if next_page is None:
                break
            page = next_page
        logger.info(
            "Finished request %s: queued=%d",
            request.params,
            queued_for_request,
        )
        return queued_for_request

    def run(self) -> int:
        total_queued = 0
        for request, found_vacancies in self._planner.plan():
            queued = self._produce_request(request)
            if queued != found_vacancies:
                logger.warning(
                    "Planner mismatch: %s planner=%d queued=%d",
                    request.params,
                    found_vacancies,
                    queued,
                )
            total_queued += queued
        logger.info(
            "Planner covered %d vacancies",
            self._planner.planned_found,
        )
        return total_queued
