from time import sleep
from typing import Callable, TypeVar

T = TypeVar("T")

def retry(
    func: Callable[..., T],
    *args,
    retries: int = 3,
    delay: float = 1.0,
    **kwargs,
) -> T:
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception:
            if attempt == retries - 1:
                raise
            sleep(delay)
    raise RuntimeError("Unreachable")
