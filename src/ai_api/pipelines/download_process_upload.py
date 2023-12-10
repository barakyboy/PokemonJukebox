# a script for downloading a youtube video, running AI over it, processing the output into gameboy inputs,
# and uploading the results to google drive

from basic_pitch.inference import predict
from utilities.Exceptions import NoInstrumentsFoundError, NoNotesFoundError
from utilities.NoteFilterStrategy import TopNVelocityStrategy,\
                        CompositeNoteFilterStrategyApplyAll, LowerFrequencyThresholdStrategy
from utilities.FrameConverter import FrameConverter
from utilities.MusicDownloader import MusicDownloader
import multiprocessing
import os
from dotenv import load_dotenv
from midi2audio import FluidSynth

load_dotenv()
MIDI_DIR = os.getenv('MIDI_DIR')
PLAYABLE_DIR = os.getenv('PLAYABLE_DIR')


def download_process_upload(link: str, fs: FluidSynth):
    """
    Takes a youtube link as input and runs AI over it and converts to gameboy inputs.
    Uploads the results to google drive (the framed notes AND .wav file)
    along with a thread object for playing the song. So adds a tuple to the queue of the form:
    (list of framed notes, tuple for playing song)
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
        mutex = multiprocessing.Lock()

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
        t = multiprocessing.Thread(target=play, args=(audio,))

        # add to queue
        q.put((framed_notes, t))

    except Exception as e:
        raise

    finally:

        # delete audio file
        mutex = multiprocessing.Lock()
        with mutex:
            if os.path.isfile(ogg_abs_path):
                os.remove(ogg_abs_path)

            if os.path.isfile(audio_abs_path):
                os.remove(audio_abs_path)

            if os.path.isfile(midi_abs_path):
                os.remove(midi_abs_path)


