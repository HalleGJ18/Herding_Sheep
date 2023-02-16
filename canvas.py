import tkinter as tk
import numpy as np
from agent import Agent

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

# draw sheep
num_of_sheep = 5
sheep_herd = []
for n in range(num_of_sheep):
    # print(b)
    sheep_herd.append(Agent(canvas))

# move sheep
for sheep in sheep_herd:
    # sheep.move_agent()
    canvas.after(30, sheep.move_agent)

# window.update()

# draw circle
# ball = canvas.create_oval(100,100,150,150, fill="red")

# # Move the ball
# xspeed=yspeed=3

# def move_ball():
#    global xspeed, yspeed

#    canvas.move(ball, xspeed, yspeed)
   
#    (leftpos, toppos, rightpos, bottompos)=canvas.coords(ball)
   
#    if leftpos <=0 or rightpos>=canvas_width:
#       xspeed=-xspeed

#    if toppos <=0 or bottompos >=canvas_height:
#       yspeed=-yspeed

#    canvas.after(30,move_ball)

# canvas.after(30, move_ball)

# main loop
window.mainloop()
