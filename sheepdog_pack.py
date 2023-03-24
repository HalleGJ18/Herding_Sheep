import numpy as np
from numpy import random
import math

from sheepdog import Sheepdog
from flock import Flock
from environment import Environment

class Pack:

    target = np.array([600.0, 600.0])

    # average position = []

    # driving or collecting
    # 0 = driving
    # 1 = collecting
    phase = 0 


    def __init__(self, n:int, e:Environment):
        self.num_of_sheepdogs = n
        self.env = e

        # call generate sheepdogs
        self.generate_sheepdogs(self.num_of_sheepdogs, self.env)

    # random start position within starting area
    # xMin, yMin, xMax, yMax bounds of start area
    def random_start_pos(self, xMin, yMin, xMax, yMax):
        xDiff = xMax-xMin
        yDiff = yMax-yMin
        p = np.array([random.rand()*xDiff + xMin, random.rand()*yDiff + yMin])
        # check if p is valid when obstacles added
        return p

    # generate sheepdogs
    def generate_sheepdogs(self, n:int, e:Environment):
        dogs = []
        dogs_posX = []
        dogs_posY = []
        for d in range(n):
            dogs.append(Sheepdog(d, e.height, e.width))
            dogs[d].set_pos(self.random_start_pos(50,50,150,150))
            dogs_posX.append(dogs[d].pos[0])
            dogs_posY.append(dogs[d].pos[1])

        self.sheepdogs = np.array(dogs)
        self.sheepdogs_positionsX = np.array(dogs_posX)
        self.sheepdogs_positionsY = np.array(dogs_posY)

    # evalute whether dogs need to collect or drive
    def determine_phase(self):
        pass

    # calculate average position
    def calc_sheepdogs_avg_pos(self):
        pass

    def drive(self):
        # position dogs such that flock is directly between them and target
        # push forwards
        pass

    def collect(self):
        # identify far sheep
        # push them towards centre of flock
        # until flock density is satisfactory
        pass
    
    # calculate sheepdogs' next moves
    def calc_next_moves(self):
        pass