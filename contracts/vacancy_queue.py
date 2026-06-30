from typing import Protocol
from models.hh import HHVacancy

class VacancyQueue(Protocol):
    def push(self, vacancy: HHVacancy) -> None:
        ...
    def pop(self, block: bool = False) -> HHVacancy | str | None:
        ...
    def close(self, worker_count: int = 1) -> None:
        ...
