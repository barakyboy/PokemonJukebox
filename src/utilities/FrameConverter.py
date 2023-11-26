from pretty_midi.pretty_midi import Note
from math import floor
from Pitch import Pitch


class FrameConverter:
    """
    A class that is responsible for converting PrettyMidi data to frames and absolute pitch class
    """

    FPS = 60
    NOTES_IN_OCTAVE = 12

    def convert_notes_to_frames(self, notes: list[Note]) -> list(tuple):
        """
        Takes an ordered (by onset) list of prettymidi notes and returns a list of 2-tuples, with
        each tuple representing the frame representing the note onset (starting from 0), and the pitch class
        of the note(i.e, of the form (frame, pitch))
        :param notes: a list of ordered (by onset) pretty_midi notes
        :return:  a list of 2-tuples, with
        each tuple representing the frame representing the note onset (starting from 0), and the pitch class
        of the note(i.e, of the form (frame, pitch))
        """

        return [(floor(note.start * self.FPS), Pitch(note.pitch % self.NOTES_IN_OCTAVE)) for note in notes]

