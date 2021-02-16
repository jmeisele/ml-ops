

from pydantic import BaseModel


class HousePredictionResult(BaseModel):
    median_house_value: int
    # model: str
    # currency: str = "USD"
