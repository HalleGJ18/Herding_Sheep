import numpy as np
from numpy import random
import math

from agent import Agent

class Sheepdog(Agent):

    velocity = np.array([1.0,1.0])

    default_vision_range = 400
    vision_range = 400 # 150?

    maintain_dist = 10 #10
    collect_dist = 2
    stop_dist = 6
    
    v_close = False

    flock_centre = 0

    sheep_in_range = False

    default_max_speed = 1.5
    max_speed = 1.5 #1.5

    # blind_angle = pi/2    # sheepdog can't see behind itself

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
        
    def set_flock_personal_space(self, d):
        self.flock_personal_space = d

    def calc_movement_to_drive_point(self):  #TODO: check the numbers this returns are what we want
        # v = self.sheep_centre - self.target
        v = self.target - self.sheep_centre
        v = v/np.linalg.norm(v)
        v = self.sheep_centre - (v * self.maintain_dist)
        # print("v: {}".format(v))
        move = v - self.pos
        move = move/np.linalg.norm(move)
        # print("move towards push point")
        # print(f"d move: {move}")
        return move


    def move_away_from_other_dogs(self, nearby_dogs): #TODO: check this returns sane numbers
        v = np.array([0.0, 0.0])
        for dog in nearby_dogs:
            dir = (self.pos - dog.pos)
            v += (dir/(np.linalg.norm(dir)**3))
        # v = v / len(nearby_dogs)
        v = v / len(nearby_dogs)
        # if np.linalg.norm(v) != 0:
        #     v = v / np.linalg.norm(v)
        # print(v)
        return v
         
    # calc sheep within given radius
    def is_a_sheep_v_close(self, sheep):
        # r is radius
        for s in sheep:
            if math.dist(self.pos, s.pos) <= self.stop_dist:
                # sheep in range
                return True
        return False
    
    # set furthest sheep
    def set_furthest_sheep(self, sheep, bool):
        self.furthest_sheep = sheep
        self.furthest_sheep_too_far = bool
        
    # collect furthest sheep
    def collect_furthest_sheep(self):
        # get vector collect_point = sheep.pos - cm
        collect_point = self.furthest_sheep.pos - self.sheep_centre
        # unit vector it, times collect_dist
        # translate to behind sheep
        collect_point = self.furthest_sheep.pos + (collect_point/np.linalg.norm(collect_point) * self.collect_dist)
        # get vector collect_point - dog.pos
        to_collect = collect_point - self.pos
        # unit vector it?
        to_collect = to_collect/np.linalg.norm(to_collect)
        return to_collect

    # calc line from target to flock centre of mass
    # find point on line where all sheep are closer to target than it
    # or, maintaining some distance from flock
    # calc most direct vector to point
    # average position of all sheepdogs should be this point


    def apply_herding(self, dogs, dog_dists):
        movement = np.array([0.0, 0.0])

        

        """if dog within 3 x personal space of a sheep, stop"""
        if self.v_close:
            self.velocity = np.array([0.0,0.0])
            # self.max_speed = 0.3*self.flock_personal_space
        
        else:
            # self.max_speed = self.default_max_speed

            """keep away from other dogs"""
            nearby_dogs = self.find_nearby(dogs, dog_dists)
            if len(nearby_dogs) > 0:
                away_from_other_dogs = self.move_away_from_other_dogs(nearby_dogs) * 35 #35
                movement += away_from_other_dogs

            if self.sheep_in_range:   
                
                """determine if drive or collect""" 
                
                # if collect
                if self.furthest_sheep_too_far:
                    # push in furthest sheep
                    to_push = self.collect_furthest_sheep()
                    # print("collect")
                    # print(f"collect: {to_push}")
                
                # else drive
                else:      
                    # move to make avg pos closer to push point
                    to_push = self.calc_movement_to_drive_point()
                    # print("drive")
                    # print(f"drive: {to_push}")
                
                
                # put it all together
                movement += to_push
            
            
        """avoid impassable obstacles"""
        movement += (self.env.avoid_impassable_obstacles(self.pos, self.velocity) * 20)
        
        if np.linalg.norm(movement) > 0:
            # print("movement change")
            self.velocity = 0.9*self.velocity + 2*movement #TODO: is this weighting what we want?

        # print(self.velocity)


