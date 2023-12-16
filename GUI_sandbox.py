# add pythonpath to searchpath. Should be path to root of project
from dotenv import load_dotenv
import os
import sys

load_dotenv()
sys.path.append(os.getenv('PYTHONPATH'))

import tkinter as tk
from game import main
from threading import Thread
from src.pipelines.add_song_to_queue import add_song_to_queue
from queue import Queue
from src.utilities.Signal import Signal
from midi2audio import FluidSynth

SOUNDFONT_PATH = os.getenv('SOUNDFONT_PATH')


# function for starting game
def start_game():
    start_game_button.pack_forget()
    game.start()


# function for getting text from label
def get_text():
    entered_text = entry.get()
    entry.delete(0, tk.END)
    print(f"spawning new thread with the link : {entered_text}")
    process_song = Thread(target=add_song_to_queue, args=(q, entered_text, fs))
    process_song.start()


# function for quiting game
def on_quit():
    sig_q.put(Signal.QUIT)
    root.destroy()



root = tk.Tk()
root.title("Game")

# initialise game queue
q = Queue()

# initialise signal queue
sig_q = Queue()

# create game thread
game = Thread(target=main, args=(q, sig_q))

# Create a button to trigger game
start_game_button = tk.Button(root, text="Start Game", command=start_game)
start_game_button.pack()

# Create field to take game links
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# program what quit button does
root.protocol("WM_DELETE_WINDOW", on_quit)

# Create a Button to trigger the action
button = tk.Button(root, text="Submit Link for Processing", command=get_text)
button.pack(pady=10)


# Start the Tkinter event loop
root.mainloop()
