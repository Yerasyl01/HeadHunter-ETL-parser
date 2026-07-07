from typing import Protocol
from models.types import Vacancy

class VacancyLoader(Protocol):
    def load(self, vacancy: Vacancy) -> None:
        ...
