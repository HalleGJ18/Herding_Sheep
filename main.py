import tkinter as tk
import numpy as np
from flock import Flock
from environment import Environment
from sheepdog import Sheepdog
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# init window
window = tk.Tk()
window.title("Herding Sheep")
window.geometry("1400x788-50-100")
window.configure(background="grey")

# define data structure
# index is time t
data = pd.DataFrame(columns=['X_Positions', 'Y_Positions'])

# instantiate environment
ENV_HEIGHT = 750
ENV_WIDTH = 750
env = Environment(ENV_HEIGHT, ENV_WIDTH)

# generate sheep
n = 100 # num of sheep
flock = Flock(n, env)

# store intial positions at t=0 in dataframe
data.loc[0] = [np.copy(flock.flock_positionsX), np.copy(flock.flock_positionsY)]


# generate sheepdog(s)
n_dogs = 1
dog  = Sheepdog(0, ENV_HEIGHT, ENV_WIDTH)
dog.set_pos(np.array([ENV_WIDTH/2,ENV_HEIGHT/2]))

T_LIMIT = 200 # num of time steps

# plot sheep moving
for t in range(1, T_LIMIT+1): # does this need to be +1?
    # update sheep
    flock.update_flock()
    # store positions
    data.loc[t] = [np.copy(flock.flock_positionsX), np.copy(flock.flock_positionsY)]


print(data)

# generate animated plot
time = 0

fig = plt.Figure(figsize=(5, 5), dpi=150)
ax = fig.add_subplot(111)
ax.set_xlim([0, ENV_WIDTH])
ax.set_ylim([0, ENV_HEIGHT])
scat = ax.scatter(data.loc[0]["X_Positions"], data.loc[0]["Y_Positions"], c='k')
scat = ax.scatter(dog.pos[0], dog.pos[1], c='r')
scatter = FigureCanvasTkAgg(fig, window)
scatter.get_tk_widget().pack()


def animate(time):
    time += 1
    if time == T_LIMIT:
        time = 0
    ax.clear()
    ax.set_xlim([0, ENV_WIDTH])
    ax.set_ylim([0, ENV_HEIGHT])
    scat = ax.scatter(data.loc[time]["X_Positions"], data.loc[time]["Y_Positions"], c='k')
    scat = ax.scatter(dog.pos[0], dog.pos[1], c='r')
    # scat.set_offsets(data.loc[time])
    return scat

ani = animation.FuncAnimation(fig, animate, repeat=True, frames=100, interval=50)

# main loop
window.mainloop()