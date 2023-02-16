import numpy as np
import math
from sheep import Sheep

class Flock:

    flock = []

    def __init__(self, n, c) -> None:
        self.num_of_sheep = n    
        self.canvas = c

        self.dists = np.zeros([self.num_of_sheep, self.num_of_sheep])
        
        # get flock of n sheep on init
        for s in range(self.num_of_sheep):
            self.flock.append(Sheep(s, self.canvas))


    def calc_distances_sheep(self):
        # create matrix of distances between sheep
        for sheep in self.flock:
            for other in self.flock:
                if sheep.id == other.id:
                    self.dists[sheep.id][other.id] = None
                else:
                    self.dists[sheep.id][other.id] = np.linalg.norm(other.pos - sheep.pos)
        # print(self.dists)


    def calc_distances_sheepdogs(self):
        # create matrix fo distances from sheepdogs
        pass

    def compare_nearby(agent):
        pass

    def calc_flocking(self):
        pass
        # loop through flock
        for sheep in self.flock:
            # call separation, alignment & cohesion calcs
            # feed in nearest neighbours
            sheep.calc_acceleration(self.flock)

    def move_flock(self):
        self.calc_distances_sheep()
        for sheep in self.flock:
            sheep.move_agent()
            # self.canvas.after(30, sheep.move_agent)
        self.canvas.after(30, self.move_flock)
