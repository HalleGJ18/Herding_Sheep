import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import math

import os

# SHEEP_CSV = "sheep_data3.csv"
# DOG_CSV = "dog_data3.csv"

# sheep_data = pd.read_csv(SHEEP_CSV, sep="|", index_col=0)
# dog_data = pd.read_csv(DOG_CSV, sep="|", index_col=0)

dir = "output"
num = "042"

DATA_CSV_NAME = dir+"/results/data"+num+".csv"
ENV_CSV_NAME = dir+"/results/env_data"+num+".csv"
OBS_CSV_NAME = dir+"/results/obstacle_data"+num+".csv"

data = pd.read_csv(DATA_CSV_NAME, sep="|", index_col=0)
env_data = pd.read_csv(ENV_CSV_NAME, sep=",", index_col=0)

obs_data = []
if os.path.exists(OBS_CSV_NAME):
    obs_data = pd.read_csv(OBS_CSV_NAME, sep=",", index_col=0)

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

# ENV_HEIGHT = 250 # 150 # 750
ENV_HEIGHT = int(env_data.loc[0]['height'])
ENV_WIDTH = int(env_data.loc[0]['width'])
# target = np.array([25.0, 25.0])

target = [float(env_data.loc[0]['target_x']), float(env_data.loc[0]['target_y'])]
target_range = float(env_data.loc[0]['target_range'])
try:	
    target_endzone = float(env_data.loc[0]['endzone'])	
    # print("true")	
except:	
    target_endzone = 25	
    # print(target_endzone)

success = env_data.loc[0]['success']

T_LIMIT = len(data.index) - 1
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
if len(obs_data) > 0:
    for i in range (len(obs_data)):
        rect = patches.Rectangle((obs_data.loc[i, 'x'], obs_data.loc[i, 'y']), obs_data.loc[i, 'width'], obs_data.loc[i, 'height'], linewidth=1, color=obs_data.loc[i, 'colour'])
        scat = ax.add_patch(rect)
    # for index, row in obs_data.iterrows():
    #     rect = patches.Rectangle((row['x'], row['y']), row['width'], row['height'], linewidth=1, color=row['colour'])
    #     scat = ax.add_patch(rect)
rect = patches.Rectangle((target[0]-target_range, target[1]-target_range), target_range*2, target_range*2, linewidth=1, edgecolor='b', facecolor='none')
scat = ax.add_patch(rect)
rect = patches.Rectangle((target[0]-target_endzone, target[1]-target_endzone), target_endzone*2, target_endzone*2, linewidth=1, edgecolor='b', facecolor='none')	
scat = ax.add_patch(rect)
scat = ax.scatter(format(data.loc[0]["sheep_x_positions"]), format(data.loc[0]["sheep_y_positions"]), c='k', s=1)
scat = ax.scatter(format(data.loc[0]["dog_x_positions"]), format(data.loc[0]["dog_y_positions"]), c='r', s=1)
scat = ax.scatter(target[0], target[1], marker="x", c="b")
scat = ax.text(0, ENV_HEIGHT, "time=0")
scatter = FigureCanvasTkAgg(fig, window)
scatter.get_tk_widget().pack()


def animate(time):
    time += 1
    if time > T_LIMIT: # used to be == ???
        time = 0
    ax.clear()
    ax.set_xlim([0, ENV_WIDTH])
    ax.set_ylim([0, ENV_HEIGHT])
    scat = ax.set_axisbelow(True)
    scat = ax.grid()
    if len(obs_data) > 0:
        for i in range (len(obs_data)):
            rect = patches.Rectangle((obs_data.loc[i, 'x'], obs_data.loc[i, 'y']), obs_data.loc[i, 'width'], obs_data.loc[i, 'height'], linewidth=1, color=obs_data.loc[i, 'colour'])
            scat = ax.add_patch(rect)
        # for index, row in obs_data.iterrows():
        #     rect = patches.Rectangle((row['x'], row['y']), row['width'], row['height'], linewidth=1, color=row['colour'])
        #     scat = ax.add_patch(rect)
    rect = patches.Rectangle((target[0]-target_range, target[1]-target_range), target_range*2, target_range*2, linewidth=1, edgecolor='b', facecolor='none')
    scat = ax.add_patch(rect)
    rect = patches.Rectangle((target[0]-target_endzone, target[1]-target_endzone), target_endzone*2, target_endzone*2, linewidth=1, edgecolor='b', facecolor='none')
    scat = ax.add_patch(rect)	
    scat = ax.scatter(format(data.loc[time]["sheep_x_positions"]), format(data.loc[time]["sheep_y_positions"]), c='k', s=1)
    scat = ax.scatter(format(data.loc[time]["dog_x_positions"]), format(data.loc[time]["dog_y_positions"]), c='r', s=1)
    scat = ax.scatter(target[0], target[1], marker="x", c="b")
    scat = ax.text(0, ENV_HEIGHT, "time="+str(time))
    return scat

ani = animation.FuncAnimation(fig, animate, repeat=False, frames=T_LIMIT, interval=60)

# main loop
window.mainloop()