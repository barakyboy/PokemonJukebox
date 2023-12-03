# a module containing exceptions pertaining to the program

class TooManyFilesError(RuntimeError):
    """
    an exception that is raised when there are too many files in a directory
    """


class NoInstrumentsFoundError(RuntimeError):
    """
    an exception that is raised when no instruments exist in PrettyMidi data
    """


class NoNotesFoundError(RuntimeError):
    """
    An exception that is raised when no notes are found by the AI
    """