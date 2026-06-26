from typing import Protocol
from models.hh import HHVacancy

class VacancyTransformer(Protocol):
    def transform(self, vacancy: HHVacancy) -> HHVacancy:
        ...
