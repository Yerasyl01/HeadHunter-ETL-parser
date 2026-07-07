import logging
from collections.abc import Iterator
from api.hh_client import HHClient
from models.search import SearchRequest
from models.hh import SearchClusterGroup, SearchCluster, SearchClusters, ClusterCandidate
from exceptions.etl import SearchPlanningError, SearchDeadEndError, GroupDeadEndError

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
        self._visited: set[frozenset[tuple[str, str]]] = set()

    @property
    def planned_found(self) -> int:
        return self._planned_found

    def _dead_end(
        self,
        request: SearchRequest,
        found: int,
        depth: int,
        *,
        group: bool,
    ) -> SearchDeadEndError:
        exc = GroupDeadEndError if group else SearchDeadEndError
        return exc(
            "Cannot split search any further. "
            f"depth={depth}"
            f"found={found}"
            f"request={request.params}"
        )

    def _cluster_score(self, cluster: SearchCluster) -> int:
        return max(
            group["count"]
            for group in cluster["groups"].values()
        )

    def _candidate_clusters(self,
        request: SearchRequest,
        search_clusters: SearchClusters,
        indent: str,
    ) -> list[ClusterCandidate]:
        candidates = []
        for name, cluster in search_clusters.items():
            if (name not in self.ALLOWED_CLUSTERS
            or name in request.params):
                continue
            if (name == "subIndustry"
            and "." in request.params.get("industry", "")):
                continue
            groups = cluster["groups"]
            if not groups:
                continue
            score = self._cluster_score(cluster)
            logger.info(
                "%sRemaining cluster %-22s groups=%3d largest=%5d",
                indent,
                name,
                len(groups),
                score
            )
            candidates.append((score, name, cluster))
        return sorted(candidates, key=lambda x: x[0])

    def _child_request(
        self,
        request: SearchRequest,
        cluster_name: str,
        group: SearchClusterGroup,
    ) -> SearchRequest:
        query = group.get("query")
        if query:
            key, value = query.split("=", 1)
            child = request.with_param(key, value)
        else:
            child = request.with_param(
                cluster_name,
                str(group["id"]),
            )
        if child.params == request.params:
            raise SearchPlanningError(
                f"Cluster '{cluster_name}' group '{group['title']}' "
                "did not modify the request."
            )
        return child

    def _plan(
        self,
        request: SearchRequest,
        parent_found: int | None = None,
        depth: int = 0,
    ) -> Iterator[tuple[SearchRequest, int]]:
        key = frozenset(request.params.items())
        if key in self._visited:
            raise self._dead_end(request, parent_found or 0, depth, group=True)
        self._visited.add(key)
        response = self._client.get_vacancies(
            request=request,
            page=0
        )
        found_vacancies = response["found"]
        if parent_found is not None and found_vacancies >= parent_found:
            raise self._dead_end(request, found_vacancies, depth, group=True)
        indent = '  ' * depth
        logger.info(
            "%sPlanning %s -> %d vacancies",
            indent,
            request.params,
            found_vacancies,
        )
        if found_vacancies <= 2000:
            self._planned_found += found_vacancies
            yield request, found_vacancies
            return

        candidates = self._candidate_clusters(
            request,
            response["search_clusters"],
            indent
        )
        if not candidates:
            raise self._dead_end(request, found_vacancies, depth, group=True)
        cluster_succeeded = False
        for index, (_, cluster_name, cluster) in enumerate(candidates, start=1):
            logger.info(
                "%sTrying cluster [%d/%d] '%s'",
                indent,
                index,
                len(candidates),
                cluster_name,
            )
            group_succeded = False
            total_groups = len(cluster["groups"])
            for i, group in enumerate(cluster["groups"].values(), start=1):
                logger.info(
                    "%s[%d/%d] %s (%d)",
                    indent,
                    i,
                    total_groups,
                    group["title"],
                    group["count"],
                )
                child = self._child_request(request, cluster_name, group)
                try:
                    for result in self._plan(child, found_vacancies, depth + 1):
                        group_succeeded = True
                        cluster_succeeded = True
                        yield result
                    logger.info(
                        "%sGroup [%d/%d] '%s' succeeded",
                        indent,
                        i,
                        total_groups,
                        group["title"],
                    )
                except GroupDeadEndError:
                    logger.info(
                        "%sGroup [%d/%d] '%s' failed",
                        indent,
                        i,
                        total_groups,
                        group["title"],
                    )
            if cluster_succeeded:
                logger.info(
                    "%sCluster [%d/%d] '%s' succeeded",
                    indent,
                    index,
                    len(candidates),
                    cluster_name,
                )
                return
            logger.info(
                "%sCluster [%d/%d] '%s' failed",
                indent,
                index,
                len(candidates),
                cluster_name,
            )
        raise self._dead_end(request, found_vacancies, depth, group=False)

    def plan(self) -> Iterator[tuple[SearchRequest, int]]:
        yield from self._plan(SearchRequest.initial())
