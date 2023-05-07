from typing import Any, Dict, Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    SQLALCHEMY_DATABASE_URI: str = None
    IEXCLOUD_API_KEY: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    REDIS_HOST: str

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