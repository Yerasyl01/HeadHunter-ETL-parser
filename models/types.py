from typing import TypeAlias

JSON: TypeAlias = (
    dict[str, "JSON"]
    | list["JSON"]
    | str
    | int
    | float
    | bool
    | None
)
QUEUE_SENTINEL="__QUEUE_CLOSED__"
