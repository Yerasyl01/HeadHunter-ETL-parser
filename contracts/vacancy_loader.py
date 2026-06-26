from typing import Protocol
from models.hh import HHVacancy

class VacancyLoader(Protocol):
    def load(self, vacancy: HHVacancy) -> None:
        ...
