from db.mongo import mongodb, MongoManager
from models.hh import HHVacancy

class MongoVacancyLoader:
    def __init__(self, mongodb: MongoManager) -> None:
        self._mongodb = mongodb

    def load(self, vacancy: HHVacancy) -> None:
        document = {
            "_id": vacancy["id"],
            **vacancy,
        }
        self._mongodb.vacancies.replace_one(
            {"_id": document["_id"]},
            document,
            upsert=True,
        )
