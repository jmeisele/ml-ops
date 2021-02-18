"""
Author: Jason Eisele
Date: February 17, 2020
Scope: Worker tasks defined
"""
import ast
from datetime import datetime

from influxdb import InfluxDBClient
from loguru import logger


def callback(ch, method, properties, body):
    # Deserialize the byte array from bytes to string and format body into dict
    body = body.decode("utf-8")
    logger.debug(f"Body: {body}")
    logger.debug(f"Data type before conversion: {type(body)}")
    body = ast.literal_eval(body)
    logger.debug(f"Data type after literal_eval: {type(body)}")


def insert_record(ch, method, properties, body):
    # Create a client object
    client = InfluxDBClient(host="influxdb",
                            port=8086,
                            username="mywriteuser",
                            password="mywritepassword",
                            database="mlopsdemo")

    # If you don't have a DB, create one with the client object
    # client.create_database("ml-ops-demo")

    # Deserialize from byte array
    body = body.decode("utf-8")

    # Convert to dict
    body = ast.literal_eval(body)
    logger.info(f"Received: {body}")

    now = datetime.now()
    now = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    json_body = [
        {
            "measurement": "predicted_house_price",
            "tags": {
                "model": body.get("model_version"),
            },
            "time": now,
            "fields": {
                "median_house_value": body.get("median_house_value")
            }
        }
    ]
    client.write_points(json_body)
    logger.info(f"Data written to influxDB")
    client.close()
