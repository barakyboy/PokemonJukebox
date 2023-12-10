# a flask microservice used to run basic-pitch AI over an mp3 file
from flask import Flask, request, jsonify
from functools import wraps
from dotenv import load_dotenv
import os
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
import tensorflow as tf
import threading
import queue

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('PYTHONANYWHERE_API_TOKEN')
app.config['PORT'] = os.getenv('PORT')
app.config['MODEL'] = tf.saved_model.load(str(ICASSP_2022_MODEL_PATH))
app.config['QUEUE'] = queue.Queue()

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


@app.route("/queue", methods=['POST'])
@key_required
def queue():

    def run_ai(song_abs_path: str):
        """
        runs the ai over the song and queues the pretty midi result.
        :param song_abs_path: the absolute path of the song the ai is running over
        """

        try:
            # run AI over video
            midi_data = predict(audio_path=song_abs_path, model_or_model_path=app.config['MODEL'])[1]
            print('finished analysing midi data')
            app.config['QUEUE'].put(midi_data)

        except Exception as e:
            app.config['QUEUE'].put(e)

        finally:
            if os.path.isfile(song_abs_path):
                os.remove(song_abs_path)



    if 'file' not in request.files:
        return jsonify({'error': 'no file key provided'}), 400

    file = request.files['file']

    # acquire lock for determining filename
    mutex = threading.Lock()

    # get a file name and save the file
    with mutex:
        i = 0
        candidate_path = os.path.join(app.config['OGG_DIR'], str(i)) + ".ogg"
        while os.path.isfile(candidate_path):
            i += 1
            candidate_path = os.path.join(app.config['OGG_DIR'], str(i)) + ".ogg"

        # save file to path
        ogg_abs_path = candidate_path
        file.save(ogg_abs_path)

    # run ai over song
    threading.Thread(target=run_ai, args=(ogg_abs_path,)).start()
    return jsonify({'message': 'successfully uploaded file, running AI over music...'}), 202


@app.route("/dequeue", methods=['GET'])
@key_required
def dequeue():
    if not app.config['QUEUE'].empty():
        head = app.config['QUEUE'].get()
        if isinstance(head, Exception):

            # exception occurred
            return jsonify({'message': 'error: an error has occurred while running AI over the data: ' + str(head)}),\
                   500
        else:
            return jsonify(head), 200
    else:
        return jsonify({'message': 'the queue is empty!'}), 202



