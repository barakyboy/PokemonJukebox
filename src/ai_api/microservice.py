# a flask microservice used to run basic-pitch AI over an mp3 file
from flask import Flask, request, jsonify, send_from_directory
from functools import wraps
from dotenv import load_dotenv
import os
import multiprocessing
from pipelines.download_process_upload import download_process_upload, PipelineStatus
import json
import uuid
import time


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('API_TOKEN')
app.config['PORT'] = os.getenv('PORT')
app.config['MAX_QUEUE_SIZE'] = os.getenv('MAX_SIZE')


MIDI_DIR = os.getenv('MIDI_DIR')
PLAYABLE_DIR = os.getenv('PLAYABLE_DIR')
PROCESSED_DIR = os.getenv('PROCESSED_DIR')
ID_DIR = os.getenv('ID_DIR')


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




def generate_unique_key():
    """
    Generates a unique string key
    :return: a unique string key
    """
    timestamp = str(int(time.time() * 1000))
    unique_id = str(uuid.uuid4().hex)
    key = timestamp + unique_id
    return key

@app.route("/queue", methods=['POST'])
@key_required
def queue():

    # initialise
    pipeline_file_path = ''

    try:

        if len(os.listdir(ID_DIR)) > app.config['MAX_QUEUE_SIZE']:
            return jsonify({'message': 'error: the queue is full — please try again later'}), 503

        # check if queue full
        data = request.get_json()

        # check that data is properly formatted
        if 'link' not in data:
            return jsonify({'message': 'error: please provide a link'}), 400

        link = data['link']



        # run ai over song
        pipeline_uuid = generate_unique_key()

        # save id to keep track
        pipeline_file_path = os.path.join(ID_DIR, pipeline_uuid)
        with open(pipeline_file_path, 'w') as file:
            file.write(PipelineStatus.RUNNING.value)

        multiprocessing.Process(target=download_process_upload, args=(link, pipeline_uuid)).start()


        # response
        return jsonify({'message': 'successfully uploaded file, running AI over music...',
                        'id': pipeline_uuid}), 202

    except Exception as e:
        # exception occurred
        if os.path.isfile(pipeline_file_path):
            os.remove(pipeline_file_path)
        return jsonify({'message': 'error: an error has occurred: ' + str(e)}), 500


@app.route("/dequeue", methods=['GET'])
@key_required
def dequeue():
    mutex = multiprocessing.Lock()
    with mutex:
        try:

            # look for a json file; if exists, get its number and associated file
            if len(os.listdir(PROCESSED_DIR)) == 0:
                return jsonify({'message': 'there are currently no files ready!'}), 202

            # if got to this point, file exists; get the associated number and data
            i = os.listdir(PROCESSED_DIR)[0].strip(".json")
            json_abs_path = os.path.join(PROCESSED_DIR, str(i)) + ".json"

            # return the dictionary version of framed notes, along with name of
            with open(json_abs_path, 'r') as json_file:
                dict_framed_notes = json.load(json_file)

                # add file id for file download
                dict_framed_notes['file_id'] = i

                # remove json file so that can dequeue other songs
                os.remove(json_abs_path)

                return jsonify(dict_framed_notes), 200

        except Exception as e:
            # exception occurred
            return jsonify({'message': 'error: an error has occurred: ' + str(e)}), 500


@app.route('/download', methods=['POST'])
@key_required
def download_wav():
    try:
        data = request.get_json()

        # check that data is properly formatted
        if 'file_id' not in data:
            return jsonify({'message': 'error: please provide a file_id'}), 400

        file_id = data['file_id']
        audio_relative_path = str(file_id) + ".wav"
        return send_from_directory(PLAYABLE_DIR, audio_relative_path)

    except Exception as e:
        # exception occurred
        return jsonify({'message': 'error: an error has occurred: ' + str(e)}), 500


@app.route('/clean', methods=['POST'])
@key_required
def clean():
    """
    a function to clean up wav file and midi file in order to free up name and space, executed after download
    """
    try:
        data = request.get_json()
        # check that data is properly formatted
        if 'file_id' not in data:
            return jsonify({'message': 'error: please provide a file_id'}), 400

        file_id = data['file_id']
        audio_abs_path = os.path.join(PLAYABLE_DIR, file_id) + ".wav"
        midi_abs_path = os.path.join(MIDI_DIR, file_id) + ".mid"

        # delete files
        os.remove(audio_abs_path)
        os.remove(midi_abs_path)

        return jsonify({"message": "successfully deleted all files"}), 200

    except Exception as e:
        # exception occurred
        return jsonify({'message': 'error: an error has occurred: ' + str(e)}), 500

@app.route("/status", methods=['POST'])
@key_required
def check_status():
    """
    Checks the status of pipelines with ids requested in JSON. If a pipeline has failed status, delete that pipeline
    id record. If
    :return:
    """

    # extract list of ids















