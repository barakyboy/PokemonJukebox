import tkinter as tk
from sandbox import main
from threading import Thread


def start_game():
    start_game_button.pack_forget()
    game.start()


root = tk.Tk()
root.title("Game")

# create game thread
game = Thread(target=main)

# Create a button to trigger link processing
start_game_button = tk.Button(root, text="Start Game", command=start_game)
start_game_button.pack()


# Start the Tkinter event loop
root.mainloop()