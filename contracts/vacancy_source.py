from collections.abc import Iterator
from typing import Protocol
from models.hh import HHVacancy

class VacancySource(Protocol):
    def extract(self) -> Iterator[HHVacancy]:
        ...
