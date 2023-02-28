import tkinter as tk
import numpy as np
from flock import Flock

# init window and canvas
window = tk.Tk()
window.title("Herding Sheep")
window.geometry("1400x788-50-100")
window.configure(background="grey")

canvas_height = 720
canvas_width = 1280
canvas = tk.Canvas(window, bg="white", height=str(canvas_height), width=str(canvas_width))
canvas.pack(pady=20)
window.update()

# generate sheep
num_of_sheep = 15
sheep_flock = Flock(num_of_sheep, canvas)

# move sheep
canvas.after(30, sheep_flock.move_flock)

# main loop
window.mainloop()
