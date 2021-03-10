"""
Author: Jason Eisele
Date: March 1, 2021
Scope: Script to generate fake data and send to our ML API
"""
import time

import requests
from sklearn import datasets

data = datasets.fetch_california_housing()

for i in range(len(data.data)):
    # Construct the request body
    array = data.data[i]
    target = data.target[i]
    body = {"median_income_in_block": array[0],
            "median_house_age_in_block": int(round(array[1])),
            "average_rooms": int(round(array[2])),
            "average_bedrooms": int(round(array[3])),
            "population_per_block": int(round(array[4])),
            "average_house_occupancy": array[5],
            "block_latitude": array[6],
            "block_longitude": array[7]
            }
    # POST request to our API
    requests.post(url="http://localhost/model/predict", json=body)
    # requests.post(url="http://localhost:8002/route", json=body)
    time.sleep(.1)
