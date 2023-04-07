from typing import Any, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.src.db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepo(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        Base Repo for work with db
        """
        self.model = model

    def get_by_id(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, offset: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(offset).limit(limit).all()
