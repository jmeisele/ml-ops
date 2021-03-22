import json
import requests

from dag_mapping import dag_config_map

from loguru import logger
from flask import Flask, request

app = Flask(__name__)


@app.route("/route", methods=["POST"])
def reroute():
    # Decode the request body
    body = request.data.decode("utf-8")

    # Convert to dict
    body = json.loads(body)
    logger.debug(f"Body: {body}")

    # Parse body for alert name on an alarm alerting state
    state = body.get("state")
    if state == "alerting":
        alert_name = body.get("ruleName")
        dag = dag_config_map.get(alert_name)

        # Set the URL depending on the dag config
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
    
    return "Training time!"


@app.route("/health", methods=["GET"])
def index():
    return "Alive!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
