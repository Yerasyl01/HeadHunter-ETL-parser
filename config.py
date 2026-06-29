import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    mongo_uri: str
    database_name: str

    hh_base_url: str
    hh_host: str
    per_page: int
    request_timeout: int

    log_level: str

    user_agent: str


settings = Settings(
    mongo_uri=os.environ["MONGO_URI"],
    database_name=os.environ["DATABASE_NAME"],

    hh_base_url=os.environ["HH_BASE_URL"],
    hh_host=os.environ["HH_HOST"],
    per_page=int(os.environ["PER_PAGE"]),
    request_timeout=int(os.environ["REQUEST_TIMEOUT"]),

    log_level=os.environ["LOG_LEVEL"],

    user_agent=os.environ["USER_AGENT"],
)
