# from pyboy import PyBoy
# from pyboy import WindowEvent
from dotenv import load_dotenv
# import os
# from pytube import YouTube
from basic_pitch.inference import predict
# from basic_pitch import ICASSP_2022_MODEL_PATH


load_dotenv()
# GAME_PATH = os.getenv('GAME_PATH')
#
# yt = YouTube('https://www.youtube.com/watch?v=SYTS2sJWcIs&ab_channel=Pokeli')
# video = yt.streams.filter(only_audio=True).first()
#
# # set up path
# current_directory = os.getcwd()
#
# # Construct the path one level up and then into the "assets" folder
# music_path = os.path.join(current_directory, "..", "assets")
#
#
# out_file = video.download(output_path=music_path)
#
# # change format to mp3
# mp3_path = os.path.join(current_directory, "..", "assets", "vid.mp3")
# os.rename(out_file, mp3_path)
# mp3_path = os.path.abspath(mp3_path)

# analyse
mp3_path = 'C:\\Users\\uriba\\Desktop\\musicmon\\assets\\my_vid.mp3'
model_output, midi_data, note_events = predict(mp3_path)
print(f' model_output: {model_output}')


# instantiate game
# with PyBoy(GAME_PATH) as pyboy:
#     while not pyboy.tick():
#         pass

# model_output, midi_data, note_events = predict()