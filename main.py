from db.mongo import mongodb
from api.client import HHClient
from etl.extract import VacancyExtractor
from etl.load import MongoVacancyLoader
from etl.runner import ETLRunner
from etl.transform import HHVacancyTransformer
from utils.logger import logger

def main() -> None:
    try:
        mongodb.connect()

        with HHClient() as client:
            runner = ETLRunner(
                source=VacancyExtractor(client),
                transformer=HHVacancyTransformer(),
                loader=MongoVacancyLoader(mongodb),
            )

            stats = runner.run()

            logger.info(stats)

    except Exception:
        logger.exception("ETL terminated unexpectedly.")
        raise


if __name__ == "__main__":
    main()
