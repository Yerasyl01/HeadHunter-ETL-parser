import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    mongo_uri: str
    database_name: str

    redis_url: str
    redis_queue_name: str

    hh_base_url: str
    hh_search_path: str
    request_timeout: int

    log_level: str

    user_agent: str
    worker_count: int


settings = Settings(
    mongo_uri=os.environ["MONGO_URI"],
    database_name=os.environ["DATABASE_NAME"],

    redis_url=os.environ["REDIS_URL"],
    redis_queue_name=os.environ["REDIS_QUEUE_NAME"],
    worker_count=int(os.environ["WORKER_COUNT"]),

    hh_base_url=os.environ["HH_BASE_URL"],
    hh_search_path=os.environ["HH_SEARCH_PATH"],
    request_timeout=int(os.environ["REQUEST_TIMEOUT"]),

    log_level=os.environ["LOG_LEVEL"],

    user_agent=os.environ["USER_AGENT"]
)
