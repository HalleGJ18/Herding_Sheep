import numpy as np
from numpy import random
import math

from sheepdog import Sheepdog
from flock import Flock
from environment import Environment

class Pack:

    # target = np.array([25.0, 25.0])
    # target = np.array([600.0, 600.0])

    # dogs_average position = []

    # driving or collecting
    # 0 = driving
    # 1 = collecting
    phase = 0 

    # dists between dog and other dogs
    # dists between dogs and sheep


    def __init__(self, n:int, e:Environment):
        self.num_of_sheepdogs = n
        self.env = e
        
        self.target = self.env.target

        # empty dists matrix
        self.dists = np.zeros([self.num_of_sheepdogs, self.num_of_sheepdogs])

        # call generate sheepdogs
        self.generate_sheepdogs(self.num_of_sheepdogs, self.env)

    # random start position within starting area
    # xMin, yMin, xMax, yMax bounds of start area
    def random_start_pos(self, xMin, yMin, xMax, yMax):
        xDiff = xMax-xMin
        yDiff = yMax-yMin
        p = np.array([random.rand()*xDiff + xMin, random.rand()*yDiff + yMin])
        # check if p is valid when obstacles added
        if self.env.check_all_obstacles(p) == False:
            p = self.random_start_pos(xMin, yMin, xMax, yMax)
            print("reroll start pos")
        return p

    # generate sheepdogs
    def generate_sheepdogs(self, n:int, e:Environment):
        dogs = []
        dogs_posX = []
        dogs_posY = []
        for d in range(n):
            dogs.append(Sheepdog(d, e))
            # dogs[d].set_pos(self.random_start_pos(13,175,27,180))
            dogs[d].set_pos(self.random_start_pos(100,200,200,225))
            dogs[d].set_target(self.target)
            dogs_posX.append(dogs[d].pos[0])
            dogs_posY.append(dogs[d].pos[1])

        # array of sheep dogs and arrays of positions
        self.sheepdogs = np.array(dogs)
        self.sheepdogs_positionsX = np.array(dogs_posX)
        self.sheepdogs_positionsY = np.array(dogs_posY)

    def calc_distances_dogs(self):
        for dog in self.sheepdogs:
            for other in self.sheepdogs:
                if dog.id == other.id:
                    self.dists[dog.id][other.id] = 0  # zero distance from self, remember to account for this later
                else:
                    self.dists[dog.id][other.id] = np.linalg.norm(other.pos - dog.pos)

    # calculate average position
    def calc_sheepdogs_avg_pos(self):
        avg_x = np.average(self.sheepdogs_positionsX)
        avg_y = np.average(self.sheepdogs_positionsY)
        return np.array(avg_x, avg_y)

    # set x and y pos of all sheep in flock
    def set_flock_pos(self, x_pos, y_pos):
        self.flock_x = x_pos
        self.flock_y = y_pos

    # store flock centre of mass
    def set_flock_centre(self, p):
        self.flock_centre = p
        for dog in self.sheepdogs:
            dog.set_flock_centre(p)  
            
    # store flock default personal space
    def set_stop_dist(self, d, n):
        # d = personal space
        # n = num of sheep
        self.flock_personal_space = d
        dog:Sheepdog
        for dog in self.sheepdogs:
            dog.set_flock_personal_space(d)
            dog.stop_dist = self.flock_personal_space * 3
            dog.maintain_dist = self.flock_personal_space * (n ** (2/3)) 
            #dog.maintain_dist = self.flock_personal_space * math.sqrt(n)
            dog.collect_dist = self.flock_personal_space 
    
    def apply_obstacle_effects(self):
        dog:Sheepdog
        for dog in self.sheepdogs:
            """apply obstacle effects"""
            if self.env.is_obstacle_reducing_movement(dog.pos):
                # print("mud")
                dog.max_speed = dog.default_max_speed * self.env.speed_reduction_factor
            else:
                dog.max_speed = dog.default_max_speed
                
            if self.env.is_obstacle_reducing_vision(dog.pos):
                # print("fog")
                dog.vision_range = dog.default_vision_range * self.env.vision_reduction_factor
            else:
                dog.vision_range = dog.default_vision_range

    def drive(self):
        # position dogs such that flock is directly between them and target
        # push forwards
        pass

    def collect(self):
        # identify far sheep
        # push them towards centre of flock
        # until flock density is satisfactory
        pass

    def calc_herding(self):
        # loop through all dogs
        for dog in self.sheepdogs:
            dog.apply_herding(self.sheepdogs, self.dists)

    # update all dogs in pack
    def update_pack(self):
        for dog in self.sheepdogs:
            
            dog.update_agent()

            np.put(self.sheepdogs_positionsX, dog.id, dog.pos[0])
            np.put(self.sheepdogs_positionsY, dog.id, dog.pos[1])