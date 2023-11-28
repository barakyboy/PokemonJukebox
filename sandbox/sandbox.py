from pyboy import PyBoy
from pyboy import WindowEvent
from dotenv import load_dotenv
import os
import time
from src.utilities.PitchControl import PitchControl
import threading
from src.utilities.Screen import Screen
from queue import Queue
from src.pipelines.add_song_to_queue import add_song_to_queue


load_dotenv()
GAME_PATH = os.getenv('GAME_PATH')

# initialise controls dictionary
release_dict = dict()
release_dict[WindowEvent.PRESS_ARROW_UP] = WindowEvent.RELEASE_ARROW_UP
release_dict[WindowEvent.PRESS_ARROW_DOWN] = WindowEvent.RELEASE_ARROW_DOWN
release_dict[WindowEvent.PRESS_ARROW_LEFT] = WindowEvent.RELEASE_ARROW_LEFT
release_dict[WindowEvent.PRESS_ARROW_RIGHT] = WindowEvent.RELEASE_ARROW_RIGHT
release_dict[WindowEvent.PRESS_BUTTON_START] = WindowEvent.RELEASE_BUTTON_START
release_dict[WindowEvent.PRESS_BUTTON_SELECT] = WindowEvent.RELEASE_BUTTON_SELECT
release_dict[WindowEvent.PRESS_BUTTON_A] = WindowEvent.RELEASE_BUTTON_A
release_dict[WindowEvent.PRESS_BUTTON_B] = WindowEvent.RELEASE_BUTTON_B

# song queue
queue = Queue()
LINK = 'https://www.youtube.com/watch?v=Xqf8jID9TsE&ab_channel=TerraBlue'

# add initial song to queue
add_song_to_queue(queue, link=LINK)

framed_notes = queue.get()

# get current note data
curr = framed_notes.pop(0)

# prepare video thread
t = threading.Thread(target=os.startfile, args=("check.mp4",))

# instantiate the gameboy screen visual
screen = Screen()

# instantiate game
with PyBoy(GAME_PATH) as pyboy:

    # initial wait for pyboy graphic to end
    time.sleep(15)

    frame_num = 0
    pitch_controller = PitchControl()

    # deal with frame 0
    if curr[0] == frame_num:

        # there is an event on this frame, execute it
        event = pitch_controller.get_control(curr[1])

        # start music
        t.start()

        for i in range(FrameConverter.HOLD_FRAMES):
            # hold for required number of frames
            pyboy.send_input(event)

            # update visual
            screen.update(event)
            # go to next frame
            frame_num += 1
            pyboy.tick()

        # release input
        pyboy.send_input(release_dict[event])

        # hold visual of last input for another frame
        screen.update(event)

        # get next input
        if len(framed_notes) == 0:
            pyboy.tick()
            exit()  # end program

        curr = framed_notes.pop(0)

    else:
        # update visual
        screen.update()

        # start music
        t.start()

    frame_num += 1

    # game loop
    while not pyboy.tick():

        # check if there is an event on this frame
        if curr[0] == frame_num:

            # there is an event on this frame, execute it
            event = pitch_controller.get_control(curr[1])

            for i in range(FrameConverter.HOLD_FRAMES):
                # hold for required number of frames
                pyboy.send_input(event)

                # update visual
                screen.update(event)
                # go to next frame
                frame_num += 1
                pyboy.tick()

            # release input
            pyboy.send_input(release_dict[event])

            # hold visual of last input for another frame
            screen.update(event)

            # get next input
            if len(framed_notes) == 0:
                pyboy.tick()
                exit()  # end program

            curr = framed_notes.pop(0)

        else:
            screen.update()

        # increment frame num
        frame_num += 1




