# -*- coding: utf-8 -*-

from flask import Flask
from services.display_routes import get_routes

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/routes", methods=['GET'])
def display():
    return get_routes()


@app.route("/urban")
def get_urban():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=True)
