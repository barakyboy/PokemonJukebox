# a flask microservice used to run basic-pitch AI over an mp3 file
from flask import Flask, request, jsonify
from functools import wraps
from dotenv import load_dotenv
import os
from src.utilities.MusicDownloader import MusicDownloader
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
import tensorflow as tf
import threading


load_dotenv()

basic_pitch_model = tf.saved_model.load(str(ICASSP_2022_MODEL_PATH))
PORT = os.getenv('PORT')

app = Flask(__name__)
app.config['MP3_DIR'] = os.getenv('MP3_DIR')
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
            return jsonify({"message": "Invalid header (token required); "
                                       "please include a key mapped to by 'Authorization'"}) , 401

        if key == app.config['SECRET_KEY']:
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "Invalid key; you are not authorised to use this service"}), 401

    return decorator


@app.route("/process_mp3", methods=['POST'])
@key_required
def process_mp3():

    if 'file' not in request.files:
        return jsonify({'error': 'no file key provided'}), 400

    file = request.files['file']

    # acquire lock for determining filename
    mutex = threading.Lock()

    # get a file name and save the file
    with mutex:
        i = 0
        candidate_path = os.path.join(app.config['MP3_DIR'], str(i)) + ".mp3"
        while os.path.isfile(candidate_path):
            i += 1
            candidate_path = os.path.join(app.config['MP3_DIR'], str(i)) + ".mp3"

        # save file to path
        mp3_abs_path = candidate_path
        file.save(mp3_abs_path)

    try:

        # run AI over video
        midi_data = predict(audio_path=mp3_abs_path, model_or_model_path=basic_pitch_model)[1]
        print('finished analysing midi data')
        return jsonify(midi_data), 200

    except Exception as e:
        return jsonify(str(e)), 500

    finally:
        if os.path.isfile(mp3_abs_path):
            os.remove(mp3_abs_path)


if __name__ == '__main__':
    app.run(port=PORT)
