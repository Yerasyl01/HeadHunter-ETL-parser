from config import settings
from exceptions.database import DatabaseConnectionError
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError

class MongoManager:
    def __init__(self) -> None:
        self._client: MongoClient | None = None
        self._database: Database | None = None

    def connect(self) -> None:
        try:
            self._client = MongoClient(settings.mongo_uri)
            self._client.admin.command("ping")
            self._database = self._client[settings.database_name]

        except PyMongoError as exc:
            raise DatabaseConnectionError(
                "Failed to connect to MongoDB."
            ) from exc

    @property
    def database(self) -> Database:
        if self._database is None:
            raise DatabaseConnectionError(
                "MongoDB has not been connected."
            )

        return self._database

    @property
    def vacancies(self) -> Collection:
        return self.database["hh_raw"]

    @property
    def metadata(self) -> Collection:
        return self.database["hh_metadata"]

mongodb = MongoManager()
