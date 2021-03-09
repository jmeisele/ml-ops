"""
Author: Jason Eisele
Date: March 9, 2021
Scope: Load test using locust, includes bad request
"""
import random

from locust import HttpUser, task
import pandas as pd
from sklearn import datasets

data = datasets.fetch_california_housing(as_frame=True).frame

feature_columns = {
    "MedInc": "median_income_in_block",
    "HouseAge": "median_house_age_in_block",
    "AveRooms": "average_rooms",
    "AveBedrms": "average_bedrooms",
    "Population": "population_per_block",
    "AveOccup": "average_house_occupancy",
    "Latitude": "block_latitude",
    "Longitude": "block_longitude",
    "MedHouseVal": "median_house_value",
}

dataset = data.rename(columns=feature_columns).drop("median_house_value", axis=1).to_dict(orient="records")


class PredictionUser(HttpUser):
    @task(1)
    def healthcheck(self):
        self.client.get("/health/heartbeat")

    @task(10)
    def prediction(self):
        record = random.choice(dataset).copy()
        self.client.post("/model/predict", json=record)

    @task(2)
    def prediction_bad_value(self):
        record = random.choice(dataset).copy()
        corrupt_key = random.choice(list(record.keys()))
        record[corrupt_key] = "bad data"
        self.client.post("/model/predict", json=record)
