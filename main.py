import tkinter as tk
import numpy as np
from flock import Flock
from environment import Environment
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
log = []

# instantiate environment
ENV_HEIGHT = 750
ENV_WIDTH = 750
env = Environment(ENV_HEIGHT, ENV_WIDTH)

# generate sheep
n = 100 # num of sheep
flock = Flock(n, env)

# store intial positions at t=0 in dataframe
data.loc[0] = [np.copy(flock.flock_positionsX), np.copy(flock.flock_positionsY)]
# log.append([np.copy(flock.flock_positionsX), np.copy(flock.flock_positionsY)])
# print(data)
# print(data.to_string())
# print(np.array(log))

# temp print to verify positions are set
# print(flock.flock_positionsX)
# print(flock.flock_positionsY)



# plot sheep moving
t_limit = 200 # num of time steps
for t in range(1, t_limit+1): # does this need to be +1?
    # update sheep
    flock.update_flock()
    # print(flock.flock_positionsX)
    # log positions
    data.loc[t] = [np.copy(flock.flock_positionsX), np.copy(flock.flock_positionsY)]
    # log.append([np.copy(flock.flock_positionsX), np.copy(flock.flock_positionsY)])


# print("break")
# log = np.array(log)
# print(log)

print(data)
# print(data.to_string())

# generate animated plot
time = 0

fig = plt.Figure(figsize=(5, 5), dpi=150)
ax = fig.add_subplot(111)
ax.set_xlim([0, ENV_WIDTH])
ax.set_ylim([0, ENV_HEIGHT])
scat = ax.scatter(data.loc[0]["X_Positions"], data.loc[0]["Y_Positions"])
# scat = ax.scatter(log[0][0], log[0][1])
scatter = FigureCanvasTkAgg(fig, window)
scatter.get_tk_widget().pack()


def animate(time):
    time += 1
    if time == 100:
        time = 0
    # print(time)
    # print(data.loc[time])
    ax.clear()
    ax.set_xlim([0, ENV_WIDTH])
    ax.set_ylim([0, ENV_HEIGHT])
    scat = ax.scatter(data.loc[time]["X_Positions"], data.loc[time]["Y_Positions"])
    # scat.set_offsets(data.loc[time])
    return scat

ani = animation.FuncAnimation(fig, animate, repeat=True, frames=100, interval=50)

# main loop
window.mainloop()