
from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    MYSQL_ROOT_PASSWORD: str = None
    MYSQL_DATABASE: str = None
    MYSQL_USER: str = None
    MYSQL_PASSWORD: str = None
    MYSQL_HOST: str = None
    MYSQL_PORT: int = None
    SQLALCHEMY_DATABASE_URI: str = None
    IEXCLOUD_API_KEY: str = None
    CELERY_BROKER_URL: str = None
    CELERY_RESULT_BACKEND: str = None
    REDIS_HOST: str = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        user = values.get('MYSQL_USER')
        password = values.get('MYSQL_PASSWORD')
        database = values.get('MYSQL_DATABASE')
        host = values.get('MYSQL_HOST')
        port = values.get('MYSQL_PORT')
        return f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"

    class Config:
        case_sensitive = True


settings = Settings()