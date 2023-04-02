from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.app.api import dependencies
from app.app.models.ticker import Ticker

router = APIRouter()

@router.get("/")
def read_items(
    db: Session = Depends(dependencies.get_db),
) -> Any:
    """
    Retrieve items.
    """
    objects  = db.query(Ticker).all()
    return {"Hello": "World"}