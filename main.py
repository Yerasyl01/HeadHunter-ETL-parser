from api.client import HHClient
from transformers.hh_vacancy_transformer import HHVacancyTransformer
from loaders.mongo_vacancy_loader import MongoVacancyLoader
from db.mongo import mongodb
from db.redis import redisdb
from queues.redis import RedisVacancyQueue
from producer.vacancy_producer import VacancyProducer
from workers.vacancy_consumer import VacancyConsumer
from concurrent.futures import ThreadPoolExecutor
from config import settings
from models.etl_stats import ETLStats
from utils.logger import logger

def main() -> None:
    try:
        mongodb.connect()
        redisdb.connect()

        queue = RedisVacancyQueue(redisdb)
        queue.clear()

        with HHClient() as client:
            producer = VacancyProducer(client, queue)
            consumers = [
                VacancyConsumer(
                    worker_id=i+1,
                    queue=queue,
                    transformer=HHVacancyTransformer(),
                    loader=MongoVacancyLoader(mongodb),
                )
                for i in range(settings.worker_count)
            ]

            with ThreadPoolExecutor(max_workers=settings.worker_count) as executor:
                futures = [
                    executor.submit(consumer.run)
                    for consumer in consumers
                ]

                queued = producer.run()
                logger.info(f"Queued {queued} vacancies")
                queue.close(settings.worker_count)

                worker_stats = [
                    future.result()
                    for future in futures
                ]

            for consumer, stats in zip(consumers, worker_stats):
                logger.info(
                    f"Worker {consumer.worker_id}: "
                    f"{stats.loaded} loaded"
                    f"({stats.duplicates} duplicates)"
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
