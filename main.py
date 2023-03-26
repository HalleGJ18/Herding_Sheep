import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

from flock import Flock
from environment import Environment
from sheepdog import Sheepdog
from sheepdog_pack import Pack

# init window
window = tk.Tk()
window.title("Herding Sheep")
window.geometry("1400x788-50-100")
window.configure(background="grey")

# define data structure
# index is time t
sheep_data = pd.DataFrame(columns=['X_Positions', 'Y_Positions'])

dog_data = pd.DataFrame(columns=['X_Positions', 'Y_Positions'])

# instantiate environment
ENV_HEIGHT = 750
ENV_WIDTH = 750
env = Environment(ENV_HEIGHT, ENV_WIDTH)

# generate sheep
n = 100 # num of sheep
flock = Flock(n, env)

# generate sheepdog(s)
n_dogs = 1 # num of dogs
pack = Pack(n_dogs, env)


# store intial positions at t=0 in dataframe
sheep_data.loc[0] = [np.copy(flock.flock_positionsX), np.copy(flock.flock_positionsY)]
dog_data.loc[0] = [np.copy(pack.sheepdogs_positionsX), np.copy(pack.sheepdogs_positionsY)]

# print("dog start pos:")
# print(pack.sheepdogs[0].pos)
# print(pack.sheepdogs[1].pos)


T_LIMIT = 200 # num of time steps

# MAIN LOOP
for t in range(1, T_LIMIT+1): # does this need to be +1?

    # update pack with flock info
    # pack.set_flock_pos()
    # pack.set_flock_centre(flock.calc_flock_centre(flock.))
    for dog in pack.sheepdogs:
        sheep_in_range = flock.get_sheep_in_area(dog.pos, dog.vision_range)
        if len(sheep_in_range) > 0:
            dog.set_seen_sheep_centre(flock.calc_sheep_centre(sheep_in_range))
            dog.sheep_in_range = True
            # print(dog.sheep_centre)
        else:
            dog.sheep_in_range = False


    # calc sheepdogs moves
    pack.calc_distances_dogs()
    
    
    pack.calc_herding()

    # calc sheep moves
    flock.calc_distances_sheep()
    flock.calc_flocking()
    
    # update sheepdog 
    pack.update_pack()

    # update sheep 
    flock.update_flock()    # if dogs updated first doesnt matter than velocity might be tangled up

    # store positions
    sheep_data.loc[t] = [np.copy(flock.flock_positionsX), np.copy(flock.flock_positionsY)]
    dog_data.loc[t] = [np.copy(pack.sheepdogs_positionsX), np.copy(pack.sheepdogs_positionsY)]


print("sheep data:")
print(sheep_data)
print("dog data:")
print(dog_data)


# generate animated plot
time = 0

fig = plt.Figure(figsize=(5, 5), dpi=150)
ax = fig.add_subplot(111)
ax.set_xlim([0, ENV_WIDTH])
ax.set_ylim([0, ENV_HEIGHT])
scat = ax.scatter(sheep_data.loc[0]["X_Positions"], sheep_data.loc[0]["Y_Positions"], c='k')
scat = ax.scatter(dog_data.loc[0]["X_Positions"], dog_data.loc[0]["Y_Positions"], c='r')
scat = ax.scatter(pack.target[0], pack.target[1], marker="x", c="b")
scatter = FigureCanvasTkAgg(fig, window)
scatter.get_tk_widget().pack()


def animate(time):
    time += 1
    if time >= T_LIMIT: # used to be == ???
        time = 0
    ax.clear()
    ax.set_xlim([0, ENV_WIDTH])
    ax.set_ylim([0, ENV_HEIGHT])
    scat = ax.scatter(sheep_data.loc[time]["X_Positions"], sheep_data.loc[time]["Y_Positions"], c='k')
    scat = ax.scatter(dog_data.loc[time]["X_Positions"], dog_data.loc[time]["Y_Positions"], c='r')
    scat = ax.scatter(pack.target[0], pack.target[1], marker="x", c="b")
    return scat

ani = animation.FuncAnimation(fig, animate, repeat=True, frames=100, interval=50)

# main loop
window.mainloop()