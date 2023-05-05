import tkinter as tk
import numpy as np
from shepherding.flock import Flock
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

root = tk.Tk()

x = np.linspace(0, 10)

fig = plt.Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
ax.set_xlim([0, 10])
scat = ax.scatter(1,0)
scatter3 = FigureCanvasTkAgg(fig, root)
scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
ax.legend(['index_price'])
ax.set_xlabel('Interest Rate')
ax.set_title('Interest Rate Vs. Index Price')

def animate(i):
    scat.set_offsets((x[i], 0))
    return scat

ani = animation.FuncAnimation(fig, animate, repeat=True, frames=len(x) - 1, interval=50)

# plt.show()

root.mainloop()