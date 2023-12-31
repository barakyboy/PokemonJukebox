# a script for downloading a youtube video, running AI over it, processing the output into gameboy inputs, and
# saving the outcome along with a wav file associated with it
import json
from basic_pitch.inference import predict
from src.utilities.Exceptions import NoInstrumentsFoundError, NoNotesFoundError
from src.utilities.NoteFilterStrategy import TopNVelocityStrategy,\
                        CompositeNoteFilterStrategyApplyAll, LowerFrequencyThresholdStrategy
from src.utilities.FrameConverter import FrameConverter
from src.utilities.MusicDownloader import MusicDownloader
import multiprocessing
import os
from dotenv import load_dotenv
from midi2audio import FluidSynth
from enum import Enum
import logging

load_dotenv()
MIDI_DIR = os.getenv('MIDI_DIR')
PLAYABLE_DIR = os.getenv('PLAYABLE_DIR')
SOUNDFONT_PATH = os.getenv('SOUNDFONT_PATH')
PROCESSED_DIR = os.getenv('PROCESSED_DIR')


class PipelineStatus(Enum):
    RUNNING = 0
    FAILED = 1
    COMPLETE = 2
    QUEUED = 3 # used to denote that the pipeline if queued on the gameboy queue


def download_process_upload(link: str, uuid_path: str, pipeline_uuid):
    """
    Takes a youtube link as input and runs AI over it and converts to gameboy inputs.
    Uploads the results to google drive (the framed notes AND .wav file)
    along with a thread object for playing the song. So adds a tuple to the queue of the form:
    (list of framed notes, tuple for playing song)
    :param link: a youtube link
    :param uuid_path: a  path of file named with string unique identifier file for pipeline
    :param pipeline_uuid: the uuid of the pipeline
    """

    # assignment for cleanup
    audio_abs_path = ''
    ogg_abs_path = ''
    midi_abs_path = ''
    json_abs_path = ''

    try:
        # download video
        downloader = MusicDownloader()
        ogg_abs_path = downloader.download_youtube_link(link)

        # run AI over video
        midi_data = predict(ogg_abs_path)[1]

        # process notes
        if len(midi_data.instruments) == 0:
            raise NoInstrumentsFoundError("Error: no instruments were analysed by the AI")

        notes = midi_data.instruments[0].notes

        if len(notes) == 0:
            raise NoNotesFoundError("Error: no notes were analysed by the AI")

        # remove pitch bends
        midi_data.instruments[0].pitch_bends = []

        # determine filtering strategy
        filter_strategy = CompositeNoteFilterStrategyApplyAll()
        filter_strategy.add_child(LowerFrequencyThresholdStrategy())
        filter_strategy.add_child(TopNVelocityStrategy())

        # filter notes according to strategy
        filtered_notes = filter_strategy.filter_notes(notes)

        # convert filtered notes to frames and pitch classes
        framed_notes = FrameConverter().convert_notes_to_frames(filtered_notes)

        # create fluidsynth instance
        fs = FluidSynth(SOUNDFONT_PATH)

        # get a filename and save files
        mutex = multiprocessing.Lock()

        midi_abs_path = os.path.join(MIDI_DIR, pipeline_uuid) + ".mid"
        midi_data.write(midi_abs_path)

        with mutex:
            # convert midi to wav
            audio_abs_path = os.path.join(PLAYABLE_DIR, pipeline_uuid) + ".wav"
            fs.midi_to_audio(midi_abs_path, audio_abs_path)

            # save framed notes
            json_abs_path = os.path.join(PROCESSED_DIR, pipeline_uuid) + ".json"
            with open(json_abs_path, 'w') as json_file:
                json_file.write(json.dumps(FrameConverter().frame_to_dic(framed_notes)))

            # mark job as complete
            with open(uuid_path, 'w') as fp:
                fp.write(str(PipelineStatus.COMPLETE.value))

        # log info
        logging.info(f"Pipeline with uuid {pipeline_uuid} completed!")

    except Exception as e:
        logging.exception(f"pipeline with uuid {pipeline_uuid} failed due to exception:\n {e}")
        # delete audio file
        mutex = multiprocessing.Lock()
        with mutex:
            if os.path.isfile(audio_abs_path):
                os.remove(audio_abs_path)
            if os.path.isfile(json_abs_path):
                os.remove(json_abs_path)

            # write failed to uuid file
            with open(uuid_path, 'w') as fp:
                fp.write(str(PipelineStatus.FAILED.value))

    finally:
        # delete audio file
        mutex = multiprocessing.Lock()
        with mutex:
            if os.path.isfile(ogg_abs_path):
                os.remove(ogg_abs_path)
            if os.path.isfile(midi_abs_path):
                os.remove(midi_abs_path)


