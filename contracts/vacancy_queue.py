from typing import Protocol
from models.types import Vacancy

class VacancyQueue(Protocol):
    def push(self, vacancy: Vacancy) -> None:
        ...
    def pop(self, block: bool = False) -> Vacancy | str | None:
        ...
    def close(self, worker_count: int = 1) -> None:
        ...
