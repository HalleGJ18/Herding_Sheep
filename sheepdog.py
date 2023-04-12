import numpy as np
from numpy import random
import math

from agent import Agent

class Sheepdog(Agent):

    velocity = np.array([10.0,10.0])

    vision_range = 150 # 750?

    maintain_dist = 10

    flock_centre = 0

    sheep_in_range = False

    # max_speed = 16

    def set_target(self, t):
        # ingest np array
        # set target
        self.target = t

    def get_target(self):
        # return np array
        return self.target
    
    def dist_to_target(self):
        # how far is dog from target
        d = math.dist(self.pos, self.target)
        return d
        
    # store flock centre of mass
    def set_flock_centre(self, p):
        self.flock_centre = p

    # store avg pos of pack
    def set_pack_avg_pos(self, p):
        # p is point
        self.pack_avg_pos = p

    # store centre of mass of sheep in visual range
    def set_seen_sheep_centre(self, p):
        # p is np array [x,y]
        self.sheep_centre = p

    def calc_movement_to_push_point(self):  #TODO: check the numbers this returns are what we want
        # v = self.sheep_centre - self.target
        v = self.target - self.sheep_centre
        v = v/np.linalg.norm(v)
        v = self.sheep_centre + (v * self.maintain_dist)
        # print("v: {}".format(v))
        move = v - self.pos
        move = move/np.linalg.norm(move)
        # print("move towards push point")
        # print(move)
        return move


    def move_away_from_other_dogs(self, nearby_dogs): #TODO: check this returns sane numbers
        v = np.array([0.0, 0.0])
        for dog in nearby_dogs:
            v += (self.pos - dog.pos)
        # v = v / len(nearby_dogs)
        v = v / len(nearby_dogs)
        v = v / np.linalg.norm(v)
        # print(v)
        return v
         


    # calc line from target to flock centre of mass
    # find point on line where all sheep are closer to target than it
    # or, maintaining some distance from flock
    # calc most direct vector to point
    # average position of all sheepdogs should be this point


    def apply_herding(self, dogs, dog_dists):
        movement = np.array([0.0, 0.0])

        # keep away from other dogs
        nearby_dogs = self.find_nearby(dogs, dog_dists)
        if len(nearby_dogs) > 0:
            away_from_other_dogs = self.move_away_from_other_dogs(nearby_dogs)
            movement += away_from_other_dogs

        # determine if drive or collect

        if self.sheep_in_range:

            # if drive
                # move to make avg pos closer to push point
            to_push = self.calc_movement_to_push_point() * 2
            

            # if collect
                # push in furthest sheep

            # put it all together
            movement += to_push
        
        if np.linalg.norm(movement) > 0:
            # print("movement change")
            self.velocity = 0.9*self.velocity + 2*movement #TODO: is this weighting what we want?

        # print(self.velocity)


