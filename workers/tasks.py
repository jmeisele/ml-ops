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
    # Decode from bytes to string
    body = body.decode("utfd-8")
    body = body.split("=")
    logger.debug({{body[0]: body[1]}})


def insert_record(ch, method, properties, body):
    # Format the json body
    body = body.decode("utf-8")
    body = body.split("=")
    now = datetime.now()
    now = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    json_body = [
        {
            "measurement": "predicted_house_price",
            # "tags": {
            #     "host": "server01",
            #     "region": "us-west"
            # },
            "time": now,
            "fields": {
                body[0]: float(body[1])
            }
        }
    ]
    # Create a client object
    client = InfluxDBClient(host="influxdb",
                            port=8086,
                            username="mywriteuser",
                            password="mywritepassword",
                            database="mlopsdemo")
    # If you don't have a DB, create one with the client object
    # client.create_database("ml-ops-demo")
    client.write_points(json_body)
