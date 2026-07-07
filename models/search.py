from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class SearchRequest:
    params: dict[str, str] = field(default_factory=dict)

    @classmethod
    def initial(cls) -> "SearchRequest":
        return cls(
            # 20 pages by 100 vacancies
            # = 2000 vacancies by request
            params={
                "ored_clusters": "true",
                "items_on_page": "100",
            #   "area": "40"
            }
        )

    def with_param(self, key: str, value: str) -> "SearchRequest":
        params = self.params.copy()
        params[key] = value
        return SearchRequest(params)

    def with_params(self, params: dict[str, str]) -> "SearchRequest":
        merged = self.params.copy()
        merged.update(params)
        return SearchRequest(merged)
