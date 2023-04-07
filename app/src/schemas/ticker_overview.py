from pydantic import BaseModel


class TickerOverview(BaseModel):
    name: str
    description: str
    country: str
    sector: str
    industry: str

    class Config:
        orm_mode = True
