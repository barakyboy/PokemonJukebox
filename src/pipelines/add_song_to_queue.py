# a pipeline to add a song to queue
from src.utilities.MusicDownloader import MusicDownloader
from basic_pitch.inference import predict
from src.utilities.exceptions import NoInstrumentsFoundError, NoNotesFoundError
from src.utilities.NoteFilterStrategy import TopNVelocityStrategy
from src.utilities.FrameConverter import FrameConverter
from queue import Queue
from src.utilities.MusicDownloader import MusicDownloader
import threading
import os
from dotenv import load_dotenv
from src.utilities.MusicPlayer import MusicPlayer


load_dotenv()
MIDI_DIR = os.getenv('MIDI_DIR')
SOUNDFONT_PATH = os.getenv('SOUNDFONT_PATH')


def add_song_to_queue(q: Queue, link: str):
    """
    Takes a queue and a youtube link as input and adds a list of framed notes corresponding to the processed link
    to the queue, along with a thread object for playing the song. So adds a tuple to the queue of the form:
    (list of framed notes, tuple for playing song)
    :param q: a queue of lists of framed notes
    :param link: a youtube link
    """

    # download video
    downloader = MusicDownloader()
    mp3_abs_path = downloader.download_youtube_link(link)

    # run AI over video
    midi_data = predict(mp3_abs_path)[1]

    # process notes
    if len(midi_data.instruments) == 0:
        os.remove(mp3_abs_path)
        raise NoInstrumentsFoundError("Error: no instruments were analysed by the AI")

    notes = midi_data.instruments[0].notes

    if len(notes) == 0:
        os.remove(mp3_abs_path)
        raise NoNotesFoundError("Error: no notes were analysed by the AI")

    # filter notes according to strategy
    filtered_notes = TopNVelocityStrategy().filter_notes(notes)

    # convert filtered notes to frames and pitch classes
    framed_notes = FrameConverter().convert_notes_to_frames(filtered_notes)

    # save midi file temporarily
    midi_abs_path = MIDI_DIR + mp3_abs_path.split(".")[0] + ".mid"
    midi_data.write(midi_abs_path)

    # create thread that plays MIDI
    mp = MusicPlayer()
    t = threading.Thread(target=mp.play_midi, args=(midi_abs_path, SOUNDFONT_PATH))

    # delete the midi file
    os.remove(midi_abs_path)

    # delete audio file
    os.remove(mp3_abs_path)

    # add to queue
    q.put((framed_notes, t))
