# a flask microservice used to run basic-pitch AI over an mp3 file
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"