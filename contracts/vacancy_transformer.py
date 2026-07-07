from typing import Protocol
from models.types import Vacancy

class VacancyTransformer(Protocol):
    def transform(self, vacancy: Vacancy) -> Vacancy:
        ...
