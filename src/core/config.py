import os
from typing import Dict, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings

load_dotenv()


class DBConfig(BaseModel):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str

    @computed_field
    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"


class CacheConfig(BaseModel):
    host: str
    port: str
    db: int = 0


class Settings(BaseSettings):
    APP_NAME: str = "Menu Bot"

    BOT_TOKEN: str = os.getenv("BOT_TOKEN")

    DATABASES: Dict[str, DBConfig] = {
        "default": DBConfig(
            DB_USER=os.getenv("DB_USER"),
            DB_PASSWORD=os.getenv("DB_PASSWORD"),
            DB_HOST=os.getenv("DB_HOST"),
            DB_NAME=os.getenv("DB_NAME")
        )
    }

    CACHES: Dict[str, CacheConfig] = {
        "default": CacheConfig(
            host=os.getenv("CACHE_HOST"),
            port=os.getenv("CACHE_PORT"),
        )
    }

    LOGGING_CONFIG: Dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'formatters': {
            'verbose': {
                'format': '%(asctime)s.%(msecs)03d | %(levelname)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'loggers': {
            'default': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }

    @property
    def DB(self) -> Optional[DBConfig]:
        return self.DATABASES.get("default")

    @property
    def CACHE(self) -> Optional[CacheConfig]:
        return self.CACHES.get("default")


settings = Settings()
