# a flask microservice used to run basic-pitch AI over an mp3 file
from flask import Flask, request, jsonify
from functools import wraps
from dotenv import load_dotenv
import os
from basic_pitch.inference import predict
import multiprocessing
from pipelines.download_process_upload import download_process_upload


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('PYTHONANYWHERE_API_TOKEN')
app.config['PORT'] = os.getenv('PORT')


MIDI_DIR = os.getenv('MIDI_DIR')
PLAYABLE_DIR = os.getenv('PLAYABLE_DIR')
PROCESSED_DIR = os.getenv('PROCESSED_DIR')


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
    try:
        data = request.get_json()

        # check that data is properly formatted
        if 'link' not in data:
            return jsonify({'message': 'error: please provide a link'}), 400

        link = data['link']

        # run ai over song
        multiprocessing.Process(target=download_process_upload(), args=(link,)).start()
        return jsonify({'message': 'successfully uploaded file, running AI over music...'}), 202

    except Exception as e:
        # exception occurred
        return jsonify({'message': 'error: an error has occurred: ' + str(e)}), 500


@app.route("/dequeue", methods=['GET'])
@key_required
def dequeue():

    try:

        mutex = multiprocessing.Lock()
        with mutex:
            # look for a midi file; if exists, get its number and associated file
            if len(os.listdir(MIDI_DIR)) == 0:
                return jsonify({'message': 'the queue is empty!'}), 202

            # if got to this point, midi file exists; get the associated number
            num_id = os.listdir(MIDI_DIR)[0].strip(".mid")


    except Exception as e:
        # exception occurred
        return jsonify({'message': 'error: an error has occurred: ' + str(e)}), 500



    if not app.config['QUEUE'].empty():
        head = app.config['QUEUE'].get()
        if isinstance(head, Exception):

            # exception occurred
            return jsonify({'message': 'error: an error has occurred while running AI over the data: ' + str(head)}),\
                   500
        else:
            return jsonify(head), 200
    else:




