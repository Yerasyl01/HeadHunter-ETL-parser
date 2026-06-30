from db.mongo import mongodb, MongoManager
from models.hh import HHVacancy

class MongoVacancyLoader:
    def __init__(self, mongodb: MongoManager) -> None:
        self._mongodb = mongodb

    def load(self, vacancy: HHVacancy) -> bool:
        document = {
            "_id": vacancy["vacancyId"],
            **vacancy,
        }
        # HH search results may overlap between adjacent pages.
        # We deduplicate by vacancyId when loading into MongoDB.
        result = self._mongodb.raw_vacancies.replace_one(
            {"_id": document["_id"]},
            document,
            upsert=True,
        )
        return result.upserted_id is None
