from contracts.vacancy_loader import VacancyLoader
from contracts.vacancy_source import VacancySource
from contracts.vacancy_transformer import VacancyTransformer
from models.etl_stats import ETLStats
from utils.logger import logger

class ETLRunner:
    def __init__(
        self,
        source: VacancySource,
        transformer: VacancyTransformer,
        loader: VacancyLoader,
    ) -> None:
        self._source = source
        self._transformer = transformer
        self._loader = loader

    def run(self) -> ETLStats:
        logger.info("Starting HH ETL")

        stats = ETLStats()

        for vacancy in self._source.extract():
            stats.extracted += 1

            vacancy = self._transformer.transform(vacancy)
            stats.transformed += 1

            self._loader.load(vacancy)
            stats.loaded += 1

        logger.info(f"Loaded {stats.loaded} vacancies.")

        return stats
