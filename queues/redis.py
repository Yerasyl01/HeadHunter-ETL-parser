import json
from db.redis import RedisManager
from contracts import VacancyQueue
from models.hh import HHVacancy
from models.types import QUEUE_SENTINEL
from config import settings


class RedisVacancyQueue(VacancyQueue):
    def __init__(self, redisdb: RedisManager):
        self._redis = redisdb

    def push(self, vacancy: HHVacancy) -> None:
        self._redis.client.rpush(
            settings.redis_queue_name,
            json.dumps(vacancy),
        )

    def pop(self, block: bool = False) -> HHVacancy | str | None:
        if block:
            result = self._redis.client.blpop(settings.redis_queue_name)
            value = None if result is None else result[1]
        else:
            value = self._redis.client.lpop(settings.redis_queue_name)

        if value is None:
            return None

        if value == QUEUE_SENTINEL:
            return QUEUE_SENTINEL
        return json.loads(value)

    def close(self, worker_count: int = 1) -> None:
        for _ in range(worker_count):
            self._redis.client.rpush(
                settings.redis_queue_name,
                QUEUE_SENTINEL,
            )

    def clear(self) -> None:
        self._redis.client.delete(settings.redis_queue_name)
