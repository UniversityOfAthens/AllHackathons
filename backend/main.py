from flask import Flask

app = Flask(__name__)


@app.route("/health")
def health():
    return "Healthy!\n"


@app.route("/ping")
def ping():
    return "Pong!\n"
