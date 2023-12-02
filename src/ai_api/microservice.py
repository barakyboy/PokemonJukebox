# a flask microservice used to run basic-pitch AI over an mp3 file
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
PORT = os.getenv('PORT')

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run(port=PORT)
