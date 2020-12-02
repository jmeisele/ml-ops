"""
Author: Jason Eisele
Date: December 2, 2020
Scope: Incoming request body data model
"""
from typing import List
from pydantic import BaseModel, Field


class HousePredictionPayload(BaseModel):
    median_income_in_block: float = Field(example=150000.00)
    median_house_age_in_block: int = Field(example=25)
    average_rooms: int = Field(example=5)
    average_bedrooms: int = Field(example=3)
    population_per_block: int = Field(example=25)
    average_house_occupancy: int = Field(example=4)
    block_latitude: float = Field(example=32.32)
    block_longitude: float = Field(example=23.23)


def payload_to_list(hpp: HousePredictionPayload) -> List:
    return [
        hpp.median_income_in_block,
        hpp.median_house_age_in_block,
        hpp.average_rooms,
        hpp.average_bedrooms,
        hpp.population_per_block,
        hpp.average_house_occupancy,
        hpp.block_latitude,
        hpp.block_longitude]
