from contracts import VacancyQueue, VacancyTransformer, VacancyLoader
from models.types import QUEUE_SENTINEL
from models.etl_stats import ETLStats

class VacancyConsumer:
    def __init__(
        self,
        worker_id: int,
        queue: VacancyQueue,
        transformer: VacancyTransformer,
        loader: VacancyLoader
    ) -> None:
        self._worker_id = worker_id
        self._queue = queue
        self._transformer = transformer
        self._loader = loader

    @property
    def worker_id(self) -> int:
        return self._worker_id

    def run(self) -> ETLStats:
        stats = ETLStats()
        while True:
            vacancy = self._queue.pop(block=True)
            if vacancy == QUEUE_SENTINEL:
                break
            assert vacancy is not None
            stats.extracted += 1

            vacancy = self._transformer.transform(vacancy)
            stats.transformed += 1

            duplicate = self._loader.load(vacancy)
            stats.loaded += 1
            if duplicate:
                stats.duplicates += 1
        return stats
