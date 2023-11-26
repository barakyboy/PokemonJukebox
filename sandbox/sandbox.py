from pyboy import PyBoy
from pyboy import WindowEvent
from dotenv import load_dotenv
import os
from pytube import YouTube
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
from src.utilities.NoteFilterStrategy import TopNVelocityStrategy
from src.utilities.FrameConverter import FrameConverter
from src.utilities.PitchControls import PitchControl


load_dotenv()
GAME_PATH = os.getenv('GAME_PATH')

yt = YouTube('https://www.youtube.com/watch?v=NTa6Xbzfq1U&ab_channel=ultragamemusic')
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

# instantiate game
with PyBoy(GAME_PATH) as pyboy:

    frame_num = 0
    pitch_controller = PitchControl()
    # game loop
    while (not pyboy.tick()) and (curr is not None) and (len(framed_notes) != 0):

        # check if there is an event on this frame
        if curr[0] == frame_num:

            # there is an event on this frame, execute it
            event = pitch_controller(curr[1])
            pyboy.send_input(event)

            # reset curr to None
            curr = framed_notes.pop(0)

        # increment frame num
        frame_num += 1




