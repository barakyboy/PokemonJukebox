from src.utilities.Pitch import Pitch
from pyboy import WindowEvent

class PitchControl:
    """
    A class that maps a pitch class to a pyboy window event
    """
    control_map = {}

    def __init__(self, pc1: Pitch = Pitch.C,
                 pc2: Pitch = Pitch.CSharp,
                 pc3: Pitch = Pitch.D,
                 pc4: Pitch = Pitch.DSharp,
                 pc5: Pitch = Pitch.E,
                 pc6: Pitch = Pitch.F,
                 pc7: Pitch = Pitch.FSharp,
                 pc8: Pitch = Pitch.G,
                 pc9: Pitch = Pitch.GSharp,
                 pc10: Pitch = Pitch.A,
                 pc11: Pitch = Pitch.ASharp,
                 pc12: Pitch = Pitch.B):
        """
        initialises the controls of the object. All pitch classes (pcs) must be distinct
        :param pc1: Pitch class that maps to PRESS_ARROW_UP
        :param pc2: Pitch class that maps to PRESS_ARROW_DOWN
        :param pc3: Pitch class that maps to PRESS_ARROW_RIGHT
        :param pc4: Pitch class that maps to PRESS_ARROW_LEFT
        :param pc5: Pitch class that maps to PRESS_BUTTON_A
        :param pc6: Pitch class that maps to PRESS_BUTTON_B
        :param pc7: Pitch class that maps to PRESS_BUTTON_SELECT
        :param pc8: Pitch class that maps to PRESS_BUTTON_START
        :param pc9: Pitch class that maps to PRESS_ARROW_UP
        :param pc10: Pitch class that maps to PRESS_ARROW_DOWN
        :param pc11: Pitch class that maps to PRESS_ARROW_RIGHT
        :param pc12: Pitch class that maps to PRESS_ARROW_LEFT
        """

        # check that input is valid
        pcs = set(pc1, pc2, pc3, pc4, pc5, pc6, pc7, pc8, pc9, pc10, pc11, pc12)
        if len(pcs) != 12:
            raise ValueError("The pitch classes must be distinct and cover entire pitch class spectrum")

        self.control_map[pc1] = WindowEvent.PRESS_ARROW_UP
        self.control_map[pc2] = WindowEvent.PRESS_ARROW_DOWN
        self.control_map[pc3] = WindowEvent.PRESS_ARROW_RIGHT
        self.control_map[pc4] = WindowEvent.PRESS_ARROW_LEFT
        self.control_map[pc5] = WindowEvent.PRESS_BUTTON_A
        self.control_map[pc6] = WindowEvent.PRESS_BUTTON_B
        self.control_map[pc7] = WindowEvent.PRESS_BUTTON_SELECT
        self.control_map[pc8] = WindowEvent.PRESS_BUTTON_START
        self.control_map[pc9] = WindowEvent.PRESS_ARROW_UP
        self.control_map[pc10] = WindowEvent.PRESS_ARROW_DOWN
        self.control_map[pc11] = WindowEvent.PRESS_ARROW_RIGHT
        self.control_map[pc12] = WindowEvent.PRESS_ARROW_LEFT

    def get_control(self, pc: Pitch):
        """
        returns the control that the pitch class maps to
        :param pc: a Pitch object
        :return: the WindowEvent control that the pitch class maps to in this object
        """


