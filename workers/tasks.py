"""
Author: Jason Eisele
Date: December 2, 2020
Scope: Worker tasks defined
"""
import uuid
import random
import time
import json
from datetime import datetime

from influxdb import InfluxDBClient
from loguru import logger


def callback(ch, method, properties, body):
    # Deserialize the byte array from bytes to string and format the json body
    body = body.decode("utf-8")
    messages = body.split(" ")
    prediction = messages[0]
    model = messages[1]
    logger.debug(f"prediction: {prediction}")
    logger.debug(f"model: {model}")
    
    # body = body.split("=")
    # logger.debug({{body[0]: body[1]}})


def insert_record(ch, method, properties, body):
    # Create a client object
    client = InfluxDBClient(host="influxdb",
                            port=8086,
                            username="mywriteuser",
                            password="mywritepassword",
                            database="mlopsdemo")
    # If you don't have a DB, create one with the client object
    # client.create_database("ml-ops-demo")

    # Deserialize from byte array and format the json body
    body = body.decode("utf-8")
    messages = body.split(" ")
    prediction = messages[0]
    model = messages[1]
    prediction_body = prediction.split("=")
    model_body = model.split("=")
    now = datetime.now()
    now = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    json_body = [
        {
            "measurement": "predicted_house_price",
            "tags": {
                "model": model_body[1],
                # "region": "us-west"
            },
            "time": now,
            "fields": {
                prediction_body[0]: float(prediction_body[1])
            }
        }
    ]
    client.write_points(json_body)
    client.close()
