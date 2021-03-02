import ast
import json
import requests

from dag_mapping import config_map

from loguru import logger
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/route", methods=["POST"])
def reroute():
    # Decode the request body and convert to dict
    body = request.data.decode("utf-8")
    # body = ast.literal_eval(body)
    logger.debug(body)

    # Set the URL depending on the dag config
    url = "http://airflow-webserver:8080/api/dags/example_bash_operator/dagRuns"

    # Payload will be blank but has to have the object with "conf" key
    payload = {"conf": {}}
    # headers =
    # response = requests.request.post(url=url, data=json.dumps(payload), headers=headers)
    # data = response.json()
    return "Got it!"


@app.route("/health", methods=["GET"])
def index():
    return "Alive!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
