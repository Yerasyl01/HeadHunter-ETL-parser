import logging
import utils.logging_config
from db.mongo import mongodb
from db.redis import redisdb
from queues.redis import RedisVacancyQueue
from api.hh_client import HHClient
from producer.search_planner import SearchPlanner
from producer.vacancy_producer import VacancyProducer
from workers.vacancy_consumer import VacancyConsumer
from bronze.transformer import VacancyTransformer
from loaders.hh_vacancy_loader import HHVacancyLoader
from concurrent.futures import ThreadPoolExecutor
from config import settings
from models.etl_stats import ETLStats

logger = logging.getLogger(__name__)

def main() -> None:
    try:
        mongodb.connect()
        redisdb.connect()

        queue = RedisVacancyQueue(redisdb)
        queue.clear()

        with HHClient() as client:
            planner = SearchPlanner(client)
            producer = VacancyProducer(client, queue, planner)
            consumers = [
                VacancyConsumer(
                    worker_id=i+1,
                    queue=queue,
                    transformer=VacancyTransformer(),
                    loader=HHVacancyLoader(mongodb),
                )
                for i in range(settings.worker_count)
            ]

            with ThreadPoolExecutor(max_workers=settings.worker_count) as executor:
                futures = [
                    executor.submit(consumer.run)
                    for consumer in consumers
                ]
                try:
                    queued = producer.run()
                    logger.info("Queued %d vacancies", queued)
                # except Exception:
                #     logger.exception("Producer failed")
                #     raise
                finally:
                    queue.close(settings.worker_count)
                worker_stats = []
                consumer_errors = []
                for future in futures:
                    try:
                        worker_stats.append(future.result())
                    except Exception as exc:
                        consumer_errors.append(exc)
                if consumer_errors:
                    raise consumer_errors[0]

            for consumer, stats in zip(consumers, worker_stats):
                logger.info(
                    "Worker %d: %d loaded (%d duplicates)",
                    consumer.worker_id,
                    stats.loaded,
                    stats.duplicates
                )
            stats = ETLStats()
            for worker_stat in worker_stats:
                stats.merge(worker_stat)
            logger.info(stats)

    except Exception:
        logger.exception("ETL terminated unexpectedly.")
        raise

if __name__ == "__main__":
    main()
