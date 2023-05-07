import math
import numpy as np
from numpy.linalg import norm
from numpy import random

from shepherding.sheep import Sheep
from shepherding.environment import Environment

class Flock:

    # flock = []
    # flock_positions = [[]]

    separation_weight = 2
    alignment_weight = 1 #0
    cohesion_weight = 1.05 #1.05
    dog_push_weight = 1
    
    default_personal_space = 2
    default_threat_range = 65 #45 #65
    default_max_speed = 1
    
    success = False

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
            sheep.append(Sheep(s, self.env))
            # sheep[s].set_pos(self.random_start_pos(75, 75, self.env.width-50, self.env.height-50))
            # sheep[s].set_pos(self.random_start_pos(75, 75, 175, 175))
            sheep[s].set_pos(self.random_start_pos(50, 50, 200, 200))
            # sheep[s].set_pos(self.random_start_pos(25, 25, 225, 225))
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
        if self.env.check_all_obstacles(p) == False:
            p = self.random_start_pos(xMin, yMin, xMax, yMax)
            # print("reroll start pos")
        return p

    def calc_distances_sheep(self):
        # create matrix of distances between sheep
        # this is a 2D array of floats, and None value if same agent
        for sheep in self.flock:
            for other in self.flock:
                if sheep.id == other.id:
                    self.dists[sheep.id][other.id] = 0  # zero distance from self, remember to account for this later
                else:
                    self.dists[sheep.id][other.id] = norm(other.pos - sheep.pos)
        # print(self.dists)

    def calc_distances_sheepdogs(self):
        # create matrix of distances from sheepdogs
        pass

    # calc sheep closest to a given point
    def calc_n_closest_sheep(self, p, n, id=None):
        # p is pos of target
        # n is the number of sheep wanted
        # id is given if a sheep is looking for other sheep, to remove itself from list
        sorted_by_dist = sorted(self.flock, key= lambda sheep: math.dist(sheep.pos, p))
        if id != None:
            sorted_by_dist = [i for i in sorted_by_dist if i.id != id]
        # check not blocked by obstacle
        # print(f"before removing can't see: {len(sorted_by_dist)}")
        if len(self.env.obstacles) > 0:
            sorted_by_dist = [j for j in sorted_by_dist if self.env.is_obstacle_blocking_vision(p,j.pos) == False]
            # print(f"after removing can't see: {len(sorted_by_dist)}")
        if len(sorted_by_dist) > n:
            sorted_by_dist = sorted_by_dist[0:n]
        return sorted_by_dist
    
    # calc sheep furthest from given point
    def calc_n_furthest_sheep(self, p, n, id=None):
        # p is pos of target
        # n is the number of sheep wanted
        # id is given if a sheep is looking for other sheep, to remove itself from list
        sorted_by_dist = sorted(self.flock, key= lambda sheep: 1/math.dist(sheep.pos, p))
        if id != None:
            sorted_by_dist = [i for i in sorted_by_dist if i.id != id]
        # check not blocked by obstacle
        # print(f"before removing can't see: {len(sorted_by_dist)}")
        if len(self.env.obstacles) > 0:
            sorted_by_dist = [j for j in sorted_by_dist if self.env.is_obstacle_blocking_vision(p,j.pos) == False]
            # print(f"after removing can't see: {len(sorted_by_dist)}")
        if len(sorted_by_dist) > n:
            sorted_by_dist = sorted_by_dist[0:n]
        return sorted_by_dist

    # calc sheep within given radius
    def get_sheep_in_area(self, p, r):
        # p is centre of area
        # r is radius
        found_sheep = []
        for s in self.flock:
            if norm(s.pos - p) <= r:
                found_sheep.append(s)
        return np.array(found_sheep)

    # calc flock centre of mass
    def calc_flock_centre(self):
        # avg x pos
        flock_avg_x = np.average(self.flock_positionsX)
        # avg y pos
        flock_avg_y = np.average(self.flock_positionsY)
        return np.array([flock_avg_x, flock_avg_y])
    
    # calc the furthest sheep from the centre of mass
    def furthest_sheep_from_cm(self, sheep):
        flock_centre = self.calc_sheep_centre(sheep)
        furthest_sheep = None
        d = 0
        for s in sheep:
            if furthest_sheep == None:
                furthest_sheep = s
                d = math.dist(flock_centre, s.pos)
            else:
                if math.dist(flock_centre, s.pos) > d:
                    furthest_sheep = s
                    d = math.dist(flock_centre, s.pos)
        return furthest_sheep, d
    
    # calc furthest sheep from target
    def furthest_sheep_from_target(self, sheep):
        furthest_sheep = None
        d = 0
        for s in sheep:
            if furthest_sheep == None:
                furthest_sheep = s
                d = math.dist(self.env.target, s.pos)
            else:
                if math.dist(self.env.target, s.pos) > d:
                    furthest_sheep = s
                    d = math.dist(self.env.target, s.pos)
        return furthest_sheep

    # calc centre of mass for an array of sheep
    def calc_sheep_centre(self, sheep):
        total_pos = np.array([0.0,0.0])
        for s in sheep:
            total_pos += s.pos
        avg_pos = total_pos / len(sheep)
        return avg_pos
    
    def apply_obstacle_effects(self):
        sheep:Sheep
        for sheep in self.flock:
            """apply obstacle effects"""
            if self.env.is_obstacle_reducing_movement(sheep.pos):
                # print("mud")
                sheep.max_speed = self.default_max_speed * self.env.speed_reduction_factor
            else:
                sheep.max_speed = self.default_max_speed
                
            if self.env.is_obstacle_reducing_vision(sheep.pos):
                # print("fog")
                sheep.vision_range = sheep.default_vision_range * self.env.vision_reduction_factor
                sheep.threat_range = self.default_threat_range * self.env.vision_reduction_factor
                # sheep.personal_space = self.default_personal_space * self.env.vision_reduction_factor
            else:
                sheep.vision_range = sheep.default_vision_range
                sheep.threat_range = self.default_threat_range 
                # sheep.personal_space = self.default_personal_space 

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
    
    # check all sheep in flock in endzone
    def check_endzone(self):
        in_endzone = True
        for sheep in self.flock:
            if self.env.in_endzone(sheep.pos) == False:
                in_endzone = False
                return False
        return True
    
    # check for success
    def check_success(self):
        # if gcm within 10 of target
        # ! and all sheep within 25 of target, or 10?
        # gcm = self.calc_flock_centre()
        # if (gcm[0] >= self.env.target[0]-self.env.target_range) and (gcm[0] <= self.env.target[0]+self.env.target_range):
        #     if (gcm[1] >= self.env.target[1]-self.env.target_range) and (gcm[1] <= self.env.target[1]+self.env.target_range):
                # check all sheep in endzone
        if self.check_endzone():
            self.success = True   

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

            # if sheep.speed != 0:
            #     print(sheep.speed)

            # log position change
            np.put(self.flock_positionsX, sheep.id, sheep.pos[0])
            np.put(self.flock_positionsY, sheep.id, sheep.pos[1])
            # self.flock_positionsX[sheep.id] = sheep.pos[0]
            # self.flock_positionsY[sheep.id] = sheep.pos[1]
            
