class ETLError(Exception):
    """Base class for ETL-related exceptions."""

class SearchPlanningError(ETLError):
    """Raised when a search cannot be partitioned further."""
