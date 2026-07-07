from collections.abc import Iterator
from typing import Protocol
from models.types import Vacancy

class VacancySource(Protocol):
    def extract(self) -> Iterator[Vacancy]:
        ...
