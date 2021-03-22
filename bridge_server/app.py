import ast
import json
import requests

from dag_mapping import dag_config_map

from loguru import logger
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/route", methods=["POST"])
def reroute():
    # Decode the request body and convert to dict
    logger.debug(type(request.data.decode("utf-8")))
    # body = request.data.decode("utf-8")
    # body = ast.literal_eval(body)
    # logger.debug(body)

    # Parse body for alert rule
    # alert_name = body.get("ruleName")
    # dag = dag_config_map.get(alert_name)

    # Set the URL depending on the dag config
    # url = f"http://localhost:8080/api/v1/dags/{dag}/dagRuns"
    url = f"http://airflow-webserver:8080/api/v1/dags/{dag}/dagRuns"

    # Payload will be blank but has to have the object with "conf" key
    payload = {"conf": {}}
    try:
        response = requests.post(
            url=url,
            json=payload,
            auth=('airflow', 'airflow')
        )
        data = response.json()
        return data
    except Exception as e:
        logger.error(f"Could not trigger Airflow DAG due to {e}")


@app.route("/health", methods=["GET"])
def index():
    return "Alive!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
