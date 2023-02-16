import numpy as np
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


    def calc_distances(self):
        pass
        # create matrix of distances between sheep
        # create matrix fo distances from sheepdogs

    def move_flock(self):
        for sheep in self.flock:
            self.canvas.after(30, sheep.move_agent)
