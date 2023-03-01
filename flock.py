import numpy as np
import math
from sheep import Sheep

class Flock:

    # flock = []

    separation_weight = 0.33
    alignment_weight = 0.33
    cohesion_weight = 0.34

    def __init__(self, n, c) -> None:
        self.num_of_sheep = n    
        self.canvas = c
        # self.flock = np.array([self.num_of_sheep])

        self.dists = np.zeros([self.num_of_sheep, self.num_of_sheep])
        
        # get flock of n sheep on init
        sheep = []
        for s in range(self.num_of_sheep):
            sheep.append(Sheep(s, self.canvas))

        self.flock = np.array(sheep)


    def calc_distances_sheep(self):
        # create matrix of distances between sheep
        # this is a 2D array of floats, and None value if same agent
        for sheep in self.flock:
            for other in self.flock:
                if sheep.id == other.id:
                    self.dists[sheep.id][other.id] = 0  # zero distance from self, remember to account for this later
                else:
                    self.dists[sheep.id][other.id] = np.linalg.norm(other.pos - sheep.pos)
        # print(self.dists)


    def calc_distances_sheepdogs(self):
        # create matrix of distances from sheepdogs
        pass


    def calc_flocking(self):        
        # loop through flock
        for sheep in self.flock:
            # call separation, alignment & cohesion calcs
            sheep.apply_flocking(self.flock, self.dists, self.separation_weight, self.alignment_weight, self.cohesion_weight)

    def move_flock(self):
        self.calc_distances_sheep()
        self.calc_flocking()
        for sheep in self.flock:
            # sheep.apply_flocking(self.flock, self.dists, self.separation_weight, self.alignment_weight, self.cohesion_weight)
            sheep.move_agent()
            # self.canvas.after(30, sheep.move_agent)
        self.canvas.after(30, self.move_flock)

    def plot_flock(self):
        pass
