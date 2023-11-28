# a pipeline to add a song to queue
from src.utilities.MusicDownloader import MusicDownloader
from basic_pitch.inference import predict
from src.utilities.exceptions import NoInstrumentsFoundError, NoNotesFoundError
from src.utilities.NoteFilterStrategy import TopNVelocityStrategy
from src.utilities.FrameConverter import FrameConverter
from queue import Queue


def add_song_to_queue(queue: Queue, link: str):
    """
    Takes a queue and a youtube link as input and adds a list of framed notes corresponding to the processed link
    to the queue
    :param queue: a queue of lists of framed notes
    :param link: a youtube link
    """

    # download video
    downloader = MusicDownloader()
    mp3_abs_path = downloader.download_youtube_link(link)

    # run AI over video
    midi_data = predict(mp3_abs_path)[1]

    # process notes
    if len(midi_data.instruments) == 0:
        raise NoInstrumentsFoundError("Error: no instruments were analysed by the AI")

    notes = midi_data.instruments[0].notes

    if len(notes) == 0:
        raise NoNotesFoundError("Error: no notes were analysed by the AI")

    # filter notes according to strategy
    filtered_notes = TopNVelocityStrategy().filter_notes(notes)

    # convert filtered notes to frames and pitch classes
    framed_notes = FrameConverter().convert_notes_to_frames(filtered_notes)

    # add to queue
    queue.queue(framed_notes)
