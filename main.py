import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import math

from flock import Flock
from environment import Environment
from sheepdog import Sheepdog
from sheepdog_pack import Pack

# init window
window = tk.Tk()
window.title("Herding Sheep")
window.geometry("1600x950+160+20")
window.configure(background="grey")

# define data structure
# index is time t
sheep_data = pd.DataFrame(columns=['sheep_x_positions', 'sheep_y_positions'])

dog_data = pd.DataFrame(columns=['dog_x_positions', 'dog_y_positions'])

# instantiate environment
ENV_HEIGHT = 250 # 150 # 750
ENV_WIDTH = 250
env = Environment(ENV_HEIGHT, ENV_WIDTH)

# generate sheep
n_sheep = 100 # num of sheep # 100
flock = Flock(n_sheep, env)

# generate sheepdog(s)
n_dogs = 2 # num of dogs
pack = Pack(n_dogs, env)


# store intial positions at t=0 in dataframe
sheep_data.loc[0] = [np.copy(flock.flock_positionsX), np.copy(flock.flock_positionsY)]
dog_data.loc[0] = [np.copy(pack.sheepdogs_positionsX), np.copy(pack.sheepdogs_positionsY)]

# print("dog start pos:")
# print(pack.sheepdogs[0].pos)
# print(pack.sheepdogs[1].pos)

# dog-sheep dist matrix
dog_sheep_dists = np.zeros([n_dogs, n_sheep])

# flock personal space
pack.set_stop_dist(flock.default_personal_space, n_sheep)
flock_rad = flock.default_personal_space * (n_sheep ** (2/3))
# print(flock_rad)

T_LIMIT = 7000 # num of time steps

success = False

# MAIN LOOP
for t in range(1, T_LIMIT+1): # does this need to be +1?
    
    """check success"""
    flock.check_success()
    if flock.success:
        print("success")
        success = True
        T_LIMIT = t-1
        break
    
    # print(f"t: {t}")
    
    """apply obstacle effects"""
    pack.apply_obstacle_effects()
    flock.apply_obstacle_effects()

    # update dog-sheep dists
    for d in pack.sheepdogs:
        for s in flock.flock:
            dog_sheep_dists[d.id][s.id] = math.dist(d.pos, s.pos)

    """update pack with flock info"""
    # pack.set_flock_pos()
    # pack.set_flock_centre(flock.calc_flock_centre(flock.))
    dog:Sheepdog
    for dog in pack.sheepdogs:
        
        sheep_in_range = flock.get_sheep_in_area(dog.pos, dog.vision_range) #TODO: update to use n closest sheep
        # sheep_in_range = flock.calc_n_closest_sheep(dog.pos, n_sheep) #20
        # print([i.id for i in sheep_in_range])
        # print(len(sheep_in_range))
        if len(sheep_in_range) > 0:
            dog.set_seen_sheep_centre(flock.calc_sheep_centre(sheep_in_range))
            dog.sheep_in_range = True
            dog.v_close = dog.is_a_sheep_v_close(sheep_in_range)
            
            # find furthest sheep
            furthest_sheep, dist = flock.furthest_sheep_from_cm(sheep_in_range)
            # print(f"furthest: {dist}")
            if dist > flock_rad:
                dog.set_furthest_sheep(furthest_sheep, True)
            else:
                dog.set_furthest_sheep(furthest_sheep, False)
            
        else:
            dog.sheep_in_range = False
            dog.v_close = False
            dog.set_furthest_sheep(None, False)
        # print("sheep in range: {}".format(dog.sheep_in_range))


    """update flock with pack info"""
    # sheep need to know if dog in range
    for sheep in flock.flock:
        seen_dogs_avg = np.array([0.0, 0.0])
        seen_dogs_count = 0
        for dog in pack.sheepdogs:
            if sheep.can_see(dog.pos, sheep.threat_range):
                seen_dogs_avg += dog.pos
                seen_dogs_count += 1
        
        # if there are dogs seen, set avg pos of dogs
        if seen_dogs_count > 0:
            seen_dogs_avg /= seen_dogs_count
            sheep.dog_in_range = True
            sheep.set_avg_dog_pos(seen_dogs_avg)

        else:
            sheep.dog_in_range = False
            



    """calc sheepdogs moves"""
    pack.calc_distances_dogs()
    pack.calc_herding()

    """calc sheep moves"""
    flock.calc_distances_sheep()
    flock.calc_flocking()
    
    """update sheepdog""" 
    pack.update_pack()

    """update sheep""" 
    flock.update_flock()    # if dogs updated first doesnt matter than velocity might be tangled up

    """store positions"""
    sheep_data.loc[t] = [np.copy(flock.flock_positionsX), np.copy(flock.flock_positionsY)]
    dog_data.loc[t] = [np.copy(pack.sheepdogs_positionsX), np.copy(pack.sheepdogs_positionsY)]  


print("sheep data:")
print(sheep_data)
print("dog data:")
print(dog_data)

# print(type(flock.flock_positionsX))
# print(type(pack.sheepdogs_positionsX))

# output to csv
result = pd.merge(sheep_data, dog_data, left_index=True, right_index=True)
result.to_csv("data.csv", encoding='utf-8', sep="|")
# sheep_data.to_csv("sheep_data.csv", encoding='utf-8', sep="|")
# dog_data.to_csv("dog_data.csv", encoding='utf-8', sep="|")

# ! output env data: dimensions, target, obstacles, success
env_data = pd.DataFrame(columns=['width', 'height', 'target_x', 'target_y', 'target_range', 'success'])
env_data.loc[0] = [env.width, env.height, env.target[0], env.target[1], env.target_range, success]
env_data.to_csv("env_data.csv", encoding='utf-8')



if len(env.obstacles) > 0:
    obstacle_data = pd.DataFrame(columns=['x', 'y', 'width', 'height', 'color'])
    index = 0
    for obstacle in env.obstacles:
        a,b,c,d,e = obstacle.export()
        obstacle_data.loc[index] = [a,b,c,d,e]
        
    obstacle_data.to_csv("obstacle_data.csv",encoding='utf-8')
    

# generate animated plot
time = 0

fig = plt.Figure(figsize=(6, 6), dpi=150)
ax = fig.add_subplot()
ax.set_xlim([0, ENV_WIDTH])
ax.set_ylim([0, ENV_HEIGHT])
scat = ax.set_axisbelow(True)
scat = ax.grid()
if len(env.obstacles) > 0:
    for obstacle in env.obstacles:
        rect = obstacle.draw()
        scat = ax.add_patch(rect)
rect = patches.Rectangle((env.target[0]-env.target_range, env.target[1]-env.target_range), env.target_range*2, env.target_range*2, linewidth=1, edgecolor='b', facecolor='none')
scat = ax.add_patch(rect)
rect = patches.Rectangle((env.target[0]-env.target_endzone, env.target[1]-env.target_endzone), env.target_endzone*2, env.target_endzone*2, linewidth=1, edgecolor='b', facecolor='none')
scat = ax.add_patch(rect)
scat = ax.scatter(sheep_data.loc[0]["sheep_x_positions"], sheep_data.loc[0]["sheep_y_positions"], c='k', s=1)
scat = ax.scatter(dog_data.loc[0]["dog_x_positions"], dog_data.loc[0]["dog_y_positions"], c='r', s=1)
scat = ax.scatter(pack.target[0], pack.target[1], marker="x", c="b")
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
    if len(env.obstacles) > 0:
        for obstacle in env.obstacles:
            rect = obstacle.draw()
            scat = ax.add_patch(rect)
    rect = patches.Rectangle((env.target[0]-env.target_range, env.target[1]-env.target_range), env.target_range*2, env.target_range*2, linewidth=1, edgecolor='b', facecolor='none')
    scat = ax.add_patch(rect)
    rect = patches.Rectangle((env.target[0]-env.target_endzone, env.target[1]-env.target_endzone), env.target_endzone*2, env.target_endzone*2, linewidth=1, edgecolor='b', facecolor='none')
    scat = ax.add_patch(rect)
    scat = ax.scatter(sheep_data.loc[time]["sheep_x_positions"], sheep_data.loc[time]["sheep_y_positions"], c='k', s=1)
    scat = ax.scatter(dog_data.loc[time]["dog_x_positions"], dog_data.loc[time]["dog_y_positions"], c='r', s=1)
    scat = ax.scatter(pack.target[0], pack.target[1], marker="x", c="b")
    scat = ax.text(0, ENV_HEIGHT, "time="+str(time))
    return scat

ani = animation.FuncAnimation(fig, animate, repeat=False, frames=T_LIMIT, interval=60)

# main loop
window.mainloop()