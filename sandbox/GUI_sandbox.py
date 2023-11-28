import tkinter as tk
from sandbox import main
from threading import Thread
from src.pipelines.add_song_to_queue import add_song_to_queue
from queue import Queue


# function for starting game
def start_game():
    start_game_button.pack_forget()
    game.start()


# function for getting text from label
def get_text():
    entered_text = entry.get()
    entry.delete(0, tk.END)
    print(f"spawning new thread with the link : {entered_text}")
    process_song = Thread(target=add_song_to_queue, args=(q, entered_text))
    process_song.start()



root = tk.Tk()
root.title("Game")

# initialise game queue
q = Queue()

# create game thread
game = Thread(target=main, args=(q,))

# Create a button to trigger game
start_game_button = tk.Button(root, text="Start Game", command=start_game)
start_game_button.pack()

# Create field to take game links
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Create a Button to trigger the action
button = tk.Button(root, text="Get Text", command=get_text)
button.pack(pady=10)



# Start the Tkinter event loop
root.mainloop()
