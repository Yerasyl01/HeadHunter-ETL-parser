class ETLError(Exception):
    """Base class for ETL-related exceptions."""

class SearchPlanningError(ETLError):
    """Base class for search planning failures."""

class SearchDeadEndError(SearchPlanningError):
    """Raised when a search cannot be partitioned any further."""

class GroupDeadEndError(SearchDeadEndError):
    """One partition (group) is unsplittable, but siblings still may succeed"""
