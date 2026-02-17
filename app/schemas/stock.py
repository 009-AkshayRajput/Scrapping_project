from pydantic import BaseModel

class StockUpdate(BaseModel):
    price: float
    volume: int
