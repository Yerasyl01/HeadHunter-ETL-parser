import httpx

class HHAPIError(Exception):
    def __init__(
        self,
        message: str,
        response: httpx.Response | None = None,
    ) -> None:
        super().__init__(message)
        self.response = response
