from dataclasses import dataclass

@dataclass(slots=True)
class ETLStats:
    extracted: int = 0
    transformed: int = 0
    loaded: int = 0
    duplicates: int = 0
    failed: int = 0

    def merge(self, other: "ETLStats") -> None:
        self.extracted += other.extracted
        self.transformed += other.transformed
        self.loaded += other.loaded
        self.duplicates += other.duplicates
        self.failed += other.failed
