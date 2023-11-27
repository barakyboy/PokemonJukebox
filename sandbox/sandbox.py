from pyboy import PyBoy
from pyboy import WindowEvent
from dotenv import load_dotenv
import os
from pytube import YouTube
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
from src.utilities.NoteFilterStrategy import TopNVelocityStrategy
from src.utilities.FrameConverter import FrameConverter
from src.utilities.PitchControl import PitchControl
from pydub import AudioSegment
from pydub.playback import play
import threading
from src.utilities.Screen import Screen

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


load_dotenv()
GAME_PATH = os.getenv('GAME_PATH')

yt = YouTube('https://www.youtube.com/watch?v=Ljqe4Nj7nBA&ab_channel=Halo2playa')
video = yt.streams.filter(only_audio=True).first()

# set up path
current_directory = os.getcwd()

# Construct the path one level up and then into the "assets" folder
music_path = os.path.join(current_directory, "..", "assets")


out_file = video.download(output_path=music_path)

# change format to mp3
mp3_path = os.path.join(current_directory, "..", "assets", "my_vid.mp3")
os.rename(out_file, mp3_path)
mp3_path = os.path.abspath(mp3_path)

# analyse
model_output, midi_data, note_events = predict(mp3_path)

# process notes
notes = midi_data.instruments[0].notes
filtered_notes = TopNVelocityStrategy().filter_notes(notes)
framed_notes = FrameConverter().convert_notes_to_frames(filtered_notes)

if len(framed_notes) == 0:
    raise ValueError("No notes registered by AI")

# get current note data
curr = framed_notes.pop(0)

sound = AudioSegment.from_file(mp3_path, format="mp4")
t = threading.Thread(target=play, args=(sound,))

# instantiate the gameboy screen visual
screen = Screen()

# instantiate game
with PyBoy(GAME_PATH) as pyboy:
    t.start()

    frame_num = 0
    pitch_controller = PitchControl()

    # deal with frame 0
    if curr[0] == frame_num:

        # there is an event on this frame, execute it
        event = pitch_controller.get_control(curr[1])
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

    frame_num += 1

    # game loop
    while not pyboy.tick():

        # check if there is an event on this frame
        if curr[0] == frame_num:

            # there is an event on this frame, execute it
            event = pitch_controller.get_control(curr[1])
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




