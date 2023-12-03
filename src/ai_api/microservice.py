# a flask microservice used to run basic-pitch AI over an mp3 file
from flask import Flask, request, jsonify
from functools import wraps
from dotenv import load_dotenv
import os
from src.utilities.MusicDownloader import MusicDownloader
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
import tensorflow as tf

load_dotenv()

basic_pitch_model = tf.saved_model.load(str(ICASSP_2022_MODEL_PATH))
PORT = os.getenv('PORT')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('PYTHONANYWHERE_API_TOKEN')


def key_required(f):
    """
    Authorization decorator
    :param f: function to be decorated
    """
    @wraps(f)
    def decorator(*args, **kwargs):

        if 'Authorization' in request.headers:
            key = request.headers['Authorization']
        else:
            return jsonify({"message": "Invalid header; please include a key mapped to by 'Authorization'"}, status=401)

        if key == app.config['SECRET_KEY']:
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "Invalid key; you are not authorised to use this service"}, status=401)

    return decorator


@app.route("/process_mp3", methods=['POST'])
@key_required
def process_link():
    return jsonify({'message': 'successfully authorized!'})
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
