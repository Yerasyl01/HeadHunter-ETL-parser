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
            self._client = MongoClient(
                settings.mongo_uri,
                serverSelectionTimeoutMS=5000
            )
            self._client.admin.command("ping")
            self._database = self._client[settings.mongo_database]

        except PyMongoError as exc:
            raise DatabaseConnectionError(
                "Failed to connect to MongoDB."
            ) from exc

    @property
    def database(self) -> Database:
        if self._database is None:
            raise DatabaseConnectionError(
                "MongoDB is not connected."
                "Call mongodb.connect() first."
            )
        return self._database

    @property
    def raw_vacancies(self) -> Collection:
        return self.database["hh_raw_vacancies"]

    @property
    def metadata(self) -> Collection:
        return self.database["hh_metadata"]

mongodb = MongoManager()
