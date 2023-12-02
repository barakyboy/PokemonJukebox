# a flask microservice used to run basic-pitch AI over an mp3 file
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from src.utilities.MusicDownloader import MusicDownloader
from basic_pitch.inference import predict

load_dotenv()
PORT = os.getenv('PORT')




app = Flask(__name__)


@app.route("/process_link", methods=['POST'])
def process_link():
    data = request.get_json()
    link = data.get('link')

    # initialise mp3 abs path
    mp3_abs_path = ''

    try:
        downloader = MusicDownloader()
        mp3_abs_path = downloader.download_youtube_link(link)

        # run AI over video
        midi_data = predict(mp3_abs_path)[1]
        return jsonify(midi_data, status=200)

    except Exception as e:
        return jsonify(str(e), 500)
    finally:
        if os.path.isfile(mp3_abs_path):
            os.remove(mp3_abs_path)


if __name__ == '__main__':
    app.run(port=PORT)
