from pretty_midi.pretty_midi import Note
from math import floor
from src.utilities.Pitch import Pitch


class FrameConverter:
    """
    A class that is responsible for converting PrettyMidi data to frames and absolute pitch class.
    Also removes notes that occur on the same frame
    """

    FPS = 60
    NOTES_IN_OCTAVE = 12
    HOLD_FRAMES = 5

    def convert_notes_to_frames(self, notes: list[Note]) -> list:
        """
        Takes an ordered (by onset) list of prettymidi notes and returns a list of 2-tuples, with
        each tuple representing the frame representing the note onset (starting from 0), and the pitch class
        of the note(i.e, of the form (frame, pitch)). Also removes notes that occur on the same frame. If two
        or more notes have the same frame, keeps the first one that occurs in the list.
        :param notes: a list of ordered (by onset) pretty_midi notes
        :return:  a list of 2-tuples, with
        each tuple representing the frame representing the note onset (starting from 0), and the pitch class
        of the note(i.e, of the form (frame, pitch)). Events will be at least two frames apart to allow for key release
        """

        framed_list = [((floor(note.start * self.FPS/(self.HOLD_FRAMES + 1)) * (self.HOLD_FRAMES + 1)),
                        Pitch(note.pitch % self.NOTES_IN_OCTAVE))
                       for note in notes]


         # remove notes that occur on the same frame
        de_dupled_list = []
        last_frame = None
        for tp in framed_list:
            frame = tp[0]
            if last_frame is None:
                # skip first frame, add it to de_duped_list
                last_frame = frame
                de_dupled_list.append(tp)
                continue
            if frame == last_frame:
                # duplicate in terms of frame
                continue
            # if made it to this point, this is a new frame
            last_frame = frame
            de_dupled_list.append(tp)

        return de_dupled_list

    def frame_to_dic(self, framed_list):
        """
        Takes a framed list and converts it to a dictionary representation
        :param framed_list: a list of (frame, Pitch)
        :return: its dictionary representation
        """
        return {str(x[0]): str(x[1].value) for x in framed_list}

    def dict_to_frame(self, dic_framed_list):
        """
        Reverses frame_to_dict; converts a dictionary representation of a framed list to a framed list
        :param dic_framed_list: dict representation of a framed list
        :return: a framed list
        """
        return sorted([(int(key), Pitch(int(val))) for key, val in dic_framed_list.items()], key=lambda x: x[0])


