from typing import TypeAlias

JSONValue: TypeAlias = (
    dict[str, "JSONValue"]
    | list["JSONValue"]
    | str
    | int
    | float
    | bool
    | None
)
JSONObject: TypeAlias = dict[str, JSONValue]

QUEUE_SENTINEL="__QUEUE_CLOSED__"
