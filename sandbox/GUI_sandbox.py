import tkinter as tk
from PIL import Image, ImageTk
from dotenv import load_dotenv
import os

load_dotenv()
IMAGE_PATH = os.getenv('GAMEBOY_IMAGE_PATH')


app = tk.Tk()
app.title("testing")

image = Image.open(IMAGE_PATH)
photo = ImageTk.PhotoImage(image)

image_label = tk.Label(app, image=photo)
image_label.pack(pady=10)

app.mainloop()