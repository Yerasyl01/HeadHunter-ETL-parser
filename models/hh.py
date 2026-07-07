from typing import Any, NotRequired, TypedDict, NamedTuple
from .types import JSONObject, Vacancy

HHVacancy = Vacancy

class SearchClusterGroup(TypedDict):
    id: str
    title: str
    count: int
    order: int
    query: NotRequired[str]
    disabled: NotRequired[bool]

class SearchCluster(TypedDict):
    groups: dict[str, SearchClusterGroup]

SearchClusters = dict[str, SearchCluster]

class HHVacancyPage(TypedDict):
    page: int
    next_page: int | None
    vacancies: list[HHVacancy]
    found: int
    search_clusters: SearchClusters

ClusterCandidate = tuple[int, str, SearchCluster]
