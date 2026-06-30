from typing import Any, NotRequired, TypedDict

HHVacancy = dict[str, Any]

class HHVacancyPage(TypedDict):
    page: int
    has_next: bool
    vacancies: list[HHVacancy]
