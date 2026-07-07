from collections import deque
from contracts import VacancyQueue
from models.types import Vacancy
from models.types import QUEUE_SENTINEL

class MemoryVacancyQueue(VacancyQueue):
    def __init__(self) -> None:
        self._queue = deque[Vacancy]()

    def push(self, vacancy: Vacancy) -> None:
        self._queue.append(vacancy)

    def pop(self) -> Vacancy | None:
        if not self._queue:
            return None
        return self._queue.popleft()

    def close(self, worker_count: int = 1) -> None:
        for _ in range(worker_count):
            self._queue.append(QUEUE_SENTINEL)
