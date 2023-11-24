from pyboy import PyBoy
from pyboy import WindowEvent

ROM_PATH = 'assets/game.gb'

# instantiate game
with PyBoy('assets/game.gb') as pyboy:
    while not pyboy.tick():
        pass
