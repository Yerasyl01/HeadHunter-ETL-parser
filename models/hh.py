from typing import Any, NotRequired, TypedDict

class HHVacancy(TypedDict):
    id: str
    name: str
    salary: NotRequired[dict[str, Any] | None]

class HHVacancyResponse(TypedDict):
    page: int
    pages: int
    items: list[HHVacancy]
