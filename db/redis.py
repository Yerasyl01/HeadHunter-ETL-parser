from redis import Redis
from redis.exceptions import RedisError
from exceptions.database import RedisConnectionError
from config import settings

class RedisManager:
    def __init__(self) -> None:
        self._client: Redis | None = None

    def connect(self) -> None:
        try:
            self._client = Redis.from_url(
                settings.redis_url,
                decode_responses=True,
            )
            self._client.ping()

        except RedisError as exc:
            raise RedisConnectionError(
                "Failed to connect to Redis."
            ) from exc

    @property
    def client(self) -> Redis:
        if self._client is None:
            raise RedisConnectionError(
                "Redis is not connected."
                "Call redisdb.connect() first."
            )
        return self._client

redisdb = RedisManager()
