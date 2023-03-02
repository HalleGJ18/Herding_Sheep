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

# instantiate environment
ENV_HEIGHT = 500
ENV_WIDTH = 500
env = Environment(ENV_HEIGHT, ENV_WIDTH)

# generate sheep
n = 5 # num of sheep
flock = Flock(n, env)

# store intial positions at t=0 in dataframe
data.loc[0] = [flock.flock_positionsX, flock.flock_positionsY]
print(data)
# print(data.to_string())

# temp print to verify positions are set
# print(flock.flock_positionsX)
# print(flock.flock_positionsY)



# plot sheep moving
t_limit = 100
for t in range(1, t_limit+1): # does this need to be +1?
    pass
    # update sheep
    # log positions


# generate animated plot
time = 0

fig = plt.Figure(figsize=(5, 5), dpi=150)
ax = fig.add_subplot(111)
ax.set_xlim([0, ENV_WIDTH])
ax.set_ylim([0, ENV_HEIGHT])
scat = ax.scatter(data.loc[time]["X_Positions"], data.loc[time]["Y_Positions"])
scatter = FigureCanvasTkAgg(fig, window)
scatter.get_tk_widget().pack()



# def animate(i):
#     scat.set_offsets((x[i], 0))
#     return scat

# ani = animation.FuncAnimation(fig, animate, repeat=True, frames=len(x) - 1, interval=50)

# main loop
window.mainloop()