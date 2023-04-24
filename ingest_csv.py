import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import math

SHEEP_CSV = "sheep_data3.csv"
DOG_CSV = "dog_data3.csv"

sheep_data = pd.read_csv(SHEEP_CSV, sep="|", index_col=0)
dog_data = pd.read_csv(DOG_CSV, sep="|", index_col=0)

# print(sheep_data)
# print(dog_data)

# print(len(sheep_data.index))
# print(dog_data.to_string())


# init window
window = tk.Tk()
window.title("Herding Sheep")
window.geometry("1400x900-1+0")
window.configure(background="grey")

# window.attributes('-fullscreen', True)

ENV_HEIGHT = 250 # 150 # 750
ENV_WIDTH = 250
target = np.array([25.0, 25.0])

T_LIMIT = len(sheep_data.index) - 1
# print(T_LIMIT)

# print(type(sheep_data.loc[0]["X_Positions"]))

# format string into np array of floats
def format(row):
  row = row[1:]
  row = row[:-1]
  row = row.split()
  row = [float(x) for x in row]
  # print(type(row))
  # print(row)
  return np.array(row)

# format(sheep_data.loc[0]["X_Positions"])

# generate animated plot
time = 0

fig = plt.Figure(figsize=(6, 6), dpi=150)
ax = fig.add_subplot()
ax.set_xlim([0, ENV_WIDTH])
ax.set_ylim([0, ENV_HEIGHT])
scat = ax.set_axisbelow(True)
scat = ax.grid()
# if len(env.obstacles) > 0:
#     for obstacle in env.obstacles:
#         rect = obstacle.draw()
#         scat = ax.add_patch(rect)
scat = ax.scatter(format(sheep_data.loc[0]["X_Positions"]), format(sheep_data.loc[0]["Y_Positions"]), c='k', s=1)
scat = ax.scatter(format(dog_data.loc[0]["X_Positions"]), format(dog_data.loc[0]["Y_Positions"]), c='r', s=1)
scat = ax.scatter(target[0], target[1], marker="x", c="b")
scat = ax.text(0, ENV_HEIGHT, "time=0")
scatter = FigureCanvasTkAgg(fig, window)
scatter.get_tk_widget().pack()


def animate(time):
    time += 1
    if time >= T_LIMIT: # used to be == ???
        time = 0
    ax.clear()
    ax.set_xlim([0, ENV_WIDTH])
    ax.set_ylim([0, ENV_HEIGHT])
    scat = ax.set_axisbelow(True)
    scat = ax.grid()
    # if len(env.obstacles) > 0:
    #     for obstacle in env.obstacles:
    #         rect = obstacle.draw()
    #         scat = ax.add_patch(rect)
    scat = ax.scatter(format(sheep_data.loc[time]["X_Positions"]), format(sheep_data.loc[time]["Y_Positions"]), c='k', s=1)
    scat = ax.scatter(format(dog_data.loc[time]["X_Positions"]), format(dog_data.loc[time]["Y_Positions"]), c='r', s=1)
    scat = ax.scatter(target[0], target[1], marker="x", c="b")
    scat = ax.text(0, ENV_HEIGHT, "time="+str(time))
    return scat

ani = animation.FuncAnimation(fig, animate, repeat=True, frames=T_LIMIT, interval=60)

# main loop
window.mainloop()