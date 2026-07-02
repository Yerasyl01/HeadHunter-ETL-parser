import logging
from collections.abc import Iterator
from api.client import HHClient
from models.search import SearchRequest
from models.hh import SearchClusters, SearchCluster
from exceptions.etl import SearchPlanningError

logger = logging.getLogger(__name__)

class SearchPlanner:
    ALLOWED_CLUSTERS = {
        "industry",
        "subIndustry",
        "professional_role",
        "experience",
        "employment_form",
        "work_format",
    }

    def __init__(self, client: HHClient) -> None:
        self._client = client
        self._planned_found = 0

    @property
    def planned_found(self) -> int:
        return self._planned_found

    def _choose_cluster(
        self,
        request: SearchRequest,
        search_clusters: SearchClusters,
        found_vacancies: int,
        depth: int,
    ) -> tuple[str, SearchCluster]:
        best_name = ""
        best_cluster = {}
        best_score = float("inf")

        for name, cluster in search_clusters.items():
            if (name not in self.ALLOWED_CLUSTERS
            or name in request.params):
                continue
            groups = cluster["groups"]
            if not groups:
                continue
            largest_bucket = max(
                group["count"]
                for group in groups.values()
            )
            logger.info(
                "Remaining cluster %-22s groups=%3d largest=%4d",
                name,
                len(groups),
                largest_bucket,
            )
            if largest_bucket < best_score:
                best_name = name
                best_cluster = cluster
                best_score = largest_bucket

        if not best_cluster:
            raise SearchPlanningError(
                "Cannot split search any further. "
                f"depth={depth}, "
                f"found={found_vacancies}, "
                f"request={request.params}"
            )
        return best_name, best_cluster

    def _plan(self, request: SearchRequest, depth: int = 0) -> Iterator[tuple[SearchRequest, int]]:
        response = self._client.get_vacancies(
            request=request,
            page=0
        )
        found_vacancies = response["found"]
        logger.info(
            "[depth=%d] Planning %s -> %d vacancies",
            depth,
            request.params,
            found_vacancies,
        )
        if found_vacancies <= 2000:
            self._planned_found += found_vacancies
            yield request, found_vacancies
            return
        cluster_name, cluster = self._choose_cluster(
            request,
            response["search_clusters"],
            found_vacancies,
            depth,
        )
        logger.info(
            "[depth=%d] Splitting %d vacancies by '%s' into %d groups",
            depth,
            found_vacancies,
            cluster_name,
            len(cluster["groups"]),
        )
        total_groups = len(cluster["groups"])
        for i, group in enumerate(cluster["groups"].values(), start=1):
            logger.info(
                "[depth=%d] [%d/%d] %s (%d)",
                depth,
                i,
                total_groups,
                group["title"],
                group["count"],
            )
            query = group.get("query")
            if query:
                key, value = query.split("=", 1)
                child = request.with_param(key, value)
            else:
                child = request.with_param(cluster_name, str(group["id"]))
            yield from self._plan(child, depth + 1)

    def plan(self) -> Iterator[tuple[SearchRequest, int]]:
        yield from self._plan(SearchRequest.initial())
