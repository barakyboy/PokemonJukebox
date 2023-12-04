# a pipeline to add a song to queue
from basic_pitch.inference import predict
from src.utilities.Exceptions import NoInstrumentsFoundError, NoNotesFoundError
from src.utilities.NoteFilterStrategy import TopNVelocityStrategy,\
                        CompositeNoteFilterStrategyApplyAll, LowerFrequencyThresholdStrategy
from src.utilities.FrameConverter import FrameConverter
from queue import Queue
from src.utilities.MusicDownloader import MusicDownloader
import threading
import os
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play
from midi2audio import FluidSynth

load_dotenv()
MIDI_DIR = os.getenv('MIDI_DIR')
PLAYABLE_DIR = os.getenv('PLAYABLE_DIR')


def add_song_to_queue(q: Queue, link: str, fs: FluidSynth):
    """
    Takes a queue and a youtube link as input and adds a list of framed notes corresponding to the processed link
    to the queue, along with a thread object for playing the song. So adds a tuple to the queue of the form:
    (list of framed notes, tuple for playing song)
    :param q: a queue of lists of framed notes
    :param link: a youtube link
    :param fs: a FluidSynth instance
    """

    # assignment for cleanup
    audio_abs_path = ''
    ogg_abs_path = ''
    midi_abs_path = ''

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

        # get a midi filename and save midi temporarily
        mutex = threading.Lock()

        with mutex:
            i = 0
            candidate_path = os.path.join(MIDI_DIR, str(i)) + ".mid"
            while os.path.isfile(candidate_path):
                i += 1
                candidate_path = os.path.join(MIDI_DIR, str(i)) + ".mid"

            midi_abs_path = candidate_path
            midi_data.write(midi_abs_path)

        # convert midi to wav
        audio_abs_path = os.path.join(PLAYABLE_DIR, str(i)) + ".wav"
        fs.midi_to_audio(midi_abs_path, audio_abs_path)

        # import wav audio
        audio = AudioSegment.from_file(audio_abs_path, format="wav")
        t = threading.Thread(target=play, args=(audio,))

        # add to queue
        q.put((framed_notes, t))

    except Exception as e:
        raise

    finally:

        # delete audio file
        mutex = threading.Lock()
        with mutex:
            if os.path.isfile(ogg_abs_path):
                os.remove(ogg_abs_path)

            if os.path.isfile(audio_abs_path):
                os.remove(audio_abs_path)

            if os.path.isfile(midi_abs_path):
                os.remove(midi_abs_path)


