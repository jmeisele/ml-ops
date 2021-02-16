from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route()
def reroute():
    return


@app.route("/health", methods=["GET"])
def index():
    return "Alive!"


if __name__ == "__main__":
    app.run(hot="0.0.0.0", port=8000, debug=True)
