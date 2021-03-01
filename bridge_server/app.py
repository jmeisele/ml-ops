import json
from requests import request
from dag_mapping import config_map

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/route", methods=["POST"])
def reroute():
    url = "http://localhost:8080/api/dags/example_bash_operator/dagRuns"
    payload = {"conf": {}}
    headers = 
    response = request.post(url=url, data=json.dumps(payload), headers=headers)
    data = response.json()


@app.route("/health", methods=["GET"])
def index():
    return "Alive!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
