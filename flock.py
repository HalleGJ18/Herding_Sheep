import numpy as np
from numpy import random

from sheep import Sheep
from environment import Environment

class Flock:

    # flock = []
    # flock_positions = [[]]

    separation_weight = 0.6
    alignment_weight = 0.5
    cohesion_weight = 0.5
    dog_push_weight = 50

    def __init__(self, n:int, e:Environment):
        self.num_of_sheep = n    
        self.env = e

        self.dists = np.zeros([self.num_of_sheep, self.num_of_sheep])
        
        # get flock of n sheep on init
        # log positions at t=0
        sheep = []
        sheep_posX = []
        sheep_posY = []
        for s in range(self.num_of_sheep):
            sheep.append(Sheep(s, self.env.height, self.env.width))
            sheep[s].set_pos(self.random_start_pos(25, 25, self.env.width-25, self.env.height-25))
            sheep_posX.append(sheep[s].pos[0])
            sheep_posY.append(sheep[s].pos[1])
            sheep[s].velocity = sheep[s].rand_velocity()

        self.flock = np.array(sheep)
        self.flock_positionsX = np.array(sheep_posX)
        self.flock_positionsY = np.array(sheep_posY)

    # random start position within starting area
    # xMin, yMin, xMax, yMax bounds of start area
    def random_start_pos(self, xMin, yMin, xMax, yMax):
        xDiff = xMax-xMin
        yDiff = yMax-yMin
        p = np.array([random.rand()*xDiff + xMin, random.rand()*yDiff + yMin])
        # check if p is valid when obstacles added
        return p

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

    # calc sheep closest to a given point
    def calc_closest_sheep(self, p):
        # p is point
        pass

    # calc sheep within given radius
    def get_sheep_in_area(self, p, r):
        # p is centre of area
        # r is radius
        found_sheep = []
        for s in self.flock:
            if np.linalg.norm(s.pos - p) <= r:
                found_sheep.append(s)
        return np.array(found_sheep)
        


    # calc flock centre of mass
    def calc_flock_centre(self):
        # avg x pos
        flock_avg_x = np.average(self.flock_positionsX)
        # avg y pos
        flock_avg_y = np.average(self.flock_positionsY)
        return np.array([flock_avg_x, flock_avg_y])
    

    # calc centre of mass for an array of sheep
    def calc_sheep_centre(self, sheep):
        total_pos = np.array([0.0,0.0])
        for s in sheep:
            total_pos += s.pos
        avg_pos = total_pos / len(sheep)
        return avg_pos

    # calc flock density
    def calc_flock_density(self): # -> float
        # calc density for whole flock
        return self.calc_density(self.flock_positionsX, self.flock_positionsY)

    def calc_density(self, x_positions, y_positions):
        # pop density = num of people / land area
        # find min and max of x and y to find the area taken up by sheep
        # do num of sheep / area

        # take arrays of x positions and y positions
        # get bottom left and top right coords
        x_min = min(x_positions)
        y_min = min(y_positions)
        x_max = max(x_positions)
        y_max = max(y_positions)
        
        # find the size of the square that contains all sheep
        area_height = y_max - y_min
        area_width = x_max - x_min
        area = area_height * area_width
        
        # calculate population density
        density:float = len(x_positions)/area
        return density

    def calc_flocking(self):        
        # loop through flock
        for sheep in self.flock:
            # call separation, alignment & cohesion calcs
            sheep.apply_flocking(self.flock, self.dists, self.separation_weight, self.alignment_weight, self.cohesion_weight, self.dog_push_weight)

    def update_flock(self):
        for sheep in self.flock:
            # update velocity 


            # update pos
            sheep.update_agent()
            # log position change
            np.put(self.flock_positionsX, sheep.id, sheep.pos[0])
            np.put(self.flock_positionsY, sheep.id, sheep.pos[1])
            # self.flock_positionsX[sheep.id] = sheep.pos[0]
            # self.flock_positionsY[sheep.id] = sheep.pos[1]
            
