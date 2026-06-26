from dataclasses import dataclass

@dataclass(slots=True)
class ETLStats:
    extracted: int = 0
    transformed: int = 0
    loaded: int = 0
    failed: int = 0
