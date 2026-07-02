from typing import Any, NotRequired, TypedDict
from .types import JSONObject

HHVacancy = JSONObject
SearchCluster = JSONObject
SearchClusters = dict[str, SearchCluster]

class HHVacancyPage(TypedDict):
    page: int
    next_page: int | None
    vacancies: list[HHVacancy]
    found: int
    search_clutsers: SearchClusters
