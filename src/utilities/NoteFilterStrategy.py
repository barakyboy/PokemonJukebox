from abc import ABC
from pretty_midi.pretty_midi import Note
from math import ceil, floor


class NoteFilterStrategy(ABC):
    """
    A class that is responsible for filtering ordered (by onset) pretty midi note lists based on some criteria
    """
    def filter_notes(self, notes: list[Note]) -> list[Note]:
        """
        filters an ordered (by onset) list of notes and returns the filtered list
        :param notes: An ordered (by onset) list of pretty midi notes
        :return: the filtered list, also ordered by onset
        """
        pass


class VelocityThresholdStrategy(NoteFilterStrategy):
    """
    A class that implements NoteFilterStrategy by giving a velocity threshold
    """

    DEFAULT_THRESHOLD = 70  # default threshold for velocity filtering

    def __init__(self, threshold: int = DEFAULT_THRESHOLD):
        """
        initialises the object with some velocity threshold
        :param threshold: a velocity threshold associated with the object, that determines the threshold
        note must exceed to be included
        """

        if (threshold < 0) or (threshold > 127):
            raise ValueError("Invalid velocity value: values must be between 0 and 127, inclusive")
        self.__threshold = threshold

    def filter_notes(self, notes: list[Note]) -> list[Note]:
        """
        filters a list of Notes based on some velocity threshold
        :param notes: A list of prettymidi notes
        :return: The input list, containing only notes with velocity exceeding the threshold of the object
        """
        return [note for note in notes if note.velocity > self.__threshold]


class TopNVelocityStrategy(NoteFilterStrategy):
    """
    A class that implements NoteFilterStrategy by choosing the top n notes for each second
    """

    DEFAULT_TOP_N = 4  # default number of top velocities chosen by top n strategy
    MAX_TOP_NOTES = 15  # maximum number of top notes allowed
    MIN_TOP_NOTES = 1  # minimum number of top notes allowed

    def __init__(self, top_n: int = DEFAULT_TOP_N):
        """
        initialises the object with some top_n value, defining the number of top notes chosen per second
        :param top_n: a number representing the number of top notes chosen per second. Must be less than or equal
        to MAX_TOP_NOTES and greater than or equal to MIN_TOP_NOTES
        """

        if (top_n < self.MIN_TOP_NOTES) or (top_n > self.MAX_TOP_NOTES):
            raise ValueError(f"Invalid top_n value: must be between {self.MIN_TOP_NOTES} and "
                             f"{self.MAX_TOP_NOTES} inclusive")
        self.__top_n = top_n

    def filter_notes(self, notes: list[Note]) -> list[Note]:
        """
        Filters a list of pretty_midi notes by choosing at most top_n notes per second.
        The notes that are chosen per second are the notes having the highest velocity values
        :param notes: a list of pretty midi notes
        :return: the filtered list of pretty midi notes, containing at most top_n notes per second
        """

        # get number of seconds considered
        num_seconds = ceil(notes[-1].end)

        # create deep copy of list
        notes_copy = notes.copy()

        # filtered list
        filtered_list = []

        # iterate over each second
        for i in range(num_seconds):

            # get sublist within that second
            j = 0
            while ((len(notes_copy) - j) != 0) and (floor(notes_copy[j].start) == i):
                j += 1

            sub_list = []
            for k in range(j):
                sub_list.append(notes_copy.pop(0))

            # append sublist to filtered list
            if len(sub_list) <= self.__top_n:
                filtered_list += sub_list
            else:
                # filtering needed
                # sort by velocity
                sorted_by_vel_n = sorted(sub_list, key=lambda note: note.velocity, reverse=True)[:self.__top_n]
                sorted_by_start = sorted(sorted_by_vel_n, key=lambda note: note.start, reverse=False)
                filtered_list += sorted_by_start

        return filtered_list


class LowerFrequencyThresholdStrategy(NoteFilterStrategy):
    """
    A class that implements NoteFilterStrategy by removing all notes below a base frequency,
    specified by its midi note number
    """

    DEFAULT_THRESHOLD = 57  # default threshold, A3

    def __init__(self, threshold: int = DEFAULT_THRESHOLD):

        """
        initialises the object with some midi note number threshold, representing pitch. All notes below it are removed.
        :param threshold: a midi_note_number threshold associated with the object, that determines the threshold
        note must exceed (or equaled to ) to be included
        """

        if (threshold < 0) or (threshold > 127):
            raise ValueError("Invalid velocity value: values must be between 0 and 127, inclusive")

        self.__threshold = threshold

    def filter_notes(self, notes: list[Note]) -> list[Note]:
        """
        filters a list of Notes based on some midi note number threshold, representing pitch
        :param notes: A list of prettymidi notes
        :return: The input list, containing only notes with pitch exceeding or equal to the threshold of the object
        """
        return [note for note in notes if note.pitch >= self.__threshold]


class CompositeNoteFilterStrategyApplyAll(NoteFilterStrategy):
    """
    The composite of the NoteFilterStrategy. Its filtering function applies all strategies.
    """

    def __init__(self):
        self.children = []

    def add_child(self, child: NoteFilterStrategy):
        """
        Adds a NoteFilterStrategy to list of note filter strategy children
        :param child: a NoteFilterStrategy
        """

        self.children.append(child)

    def filter_notes(self, notes: list[Note]) -> list[Note]:
        """
        Filters a list of pretty midi notes by applying all child strategies. They are applied in the order
        they are added.
        :param notes: a list of pretty midi notes
        :return: the list of pretty midi notes after having every strategy applied
        """
        for strategy in self.children:
            notes = strategy.filter_notes(notes)

        return notes





