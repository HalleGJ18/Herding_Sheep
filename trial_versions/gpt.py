import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create some random data for the scatter plot
N = 50
x = np.random.rand(N)
y = np.random.rand(N)
colors = np.random.rand(N)
sizes = 1000 * np.random.rand(N)

# Set up the figure and axis
fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=colors, s=sizes, alpha=0.3)

# Define the animation function
def update(N):
    # Generate new random data for the scatter plot
    new_x = np.random.rand(N)
    new_y = np.random.rand(N)
    # new_colors = np.random.rand(N)
    # new_sizes = 1000 * np.random.rand(N)
    
    # Update the scatter plot with the new data
    scatter.set_offsets(np.c_[new_x, new_y])
    # scatter.set_color(new_colors)
    # scatter.set_sizes(new_sizes)
    
    # Return the updated scatter plot
    return scatter,

# Set up the animation
ani = animation.FuncAnimation(fig, update, frames=10, interval=500, blit=True)

# Show the animation
plt.show()
