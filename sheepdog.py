import numpy as np
from numpy import random
from numpy.linalg import norm
import math

from agent import Agent

class Sheepdog(Agent):

    velocity = np.array([1.0,1.0])

    default_vision_range = 100
    vision_range = 100 # 150?
    
    personal_space = 100

    maintain_dist = 10 #10
    collect_dist = 2
    stop_dist = 6
    
    v_close = False

    flock_centre = 0

    sheep_in_range = False

    default_max_speed = 1.5
    max_speed = 1.5 #1.5
    
    weight_a = 10
    weight_b = 200
    weight_c = 8
    weight_d = 1000

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
        v = v/norm(v)
        v = self.sheep_centre - (v * self.maintain_dist)
        # print("v: {}".format(v))
        move = v - self.pos
        move = move/norm(move)
        # print("move towards push point")
        # print(f"d move: {move}")
        return move


    def move_away_from_other_dogs(self, nearby_dogs): #TODO: check this returns sane numbers
        v = np.array([0.0, 0.0])
        for dog in nearby_dogs:
            # print(f"self id: {self.id}, dog id: {dog.id}")
            d = math.dist(self.pos,dog.pos)
            # if d <= self.personal_space: #! only care about other dogs being close if theyre very close
            dir  = (self.pos - dog.pos) # *(1/d)
            v += (dir/(norm(dir)**3)) #! weight inversely to dist between dogs 
                # v += (self.pos - dog.pos) 
        v = v / len(nearby_dogs)
        # if norm(v) != 0:
        #     v = v / norm(v) # remove zero magnitude check?
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
    def set_furthest_sheep(self, sheep):
        self.furthest_sheep = sheep
        # self.furthest_sheep_too_far = bool
        
    # collect furthest sheep
    def collect_furthest_sheep(self):
        # get vector collect_point = sheep.pos - cm
        collect_point = self.furthest_sheep.pos - self.sheep_centre
        # unit vector it, times collect_dist
        # translate to behind sheep
        collect_point = self.furthest_sheep.pos + (collect_point/norm(collect_point) * self.collect_dist)
        # get vector collect_point - dog.pos
        to_collect = collect_point - self.pos
        # unit vector it?
        to_collect = to_collect/norm(to_collect)
        return to_collect
    
    # push furthest sheep towards target
    def push_furthest_sheep(self):
        pass

    # calc line from target to flock centre of mass
    # find point on line where all sheep are closer to target than it
    # or, maintaining some distance from flock
    # calc most direct vector to point
    # average position of all sheepdogs should be this point


    def apply_herding(self, dogs, dog_dists):
        movement = np.array([0.0, 0.0])

        """keep away from other dogs"""
        # D: away from sheepdogs
        nearby_dogs = self.find_nearby(dogs, dog_dists)
        if len(nearby_dogs) > 0:
            away_from_other_dogs = self.move_away_from_other_dogs(nearby_dogs)  * self.weight_d #* (1/len(nearby_dogs))
            movement += away_from_other_dogs

        if self.sheep_in_range:   
                
            """determine if drive or collect""" 
            
            # A: chase furthest sheep
            # chase_sheep = self.furthest_sheep.pos - self.pos
            chase_sheep = self.pos - self.furthest_sheep.pos
            if norm(chase_sheep) != 0:
                chase_sheep = chase_sheep/norm(chase_sheep)
            chase_sheep *= -1
                
            # B: keep slightly away from furthest sheep
            # away_from_sheep = self.pos - self.furthest_sheep.pos
            away_from_sheep = self.furthest_sheep.pos - self.pos
            if norm(away_from_sheep) != 0:
                away_from_sheep = away_from_sheep/(norm(away_from_sheep)**3)
            # away_from_sheep *= -1
                
            # C: keep away from goal
            away_from_goal = self.pos - self.env.target
            if norm(away_from_goal) != 0:
                away_from_goal = away_from_goal/norm(away_from_goal)
            # away_from_goal *= -1  # ? dont know but its what the paper says
            
            # put it all together
            movement = movement + (chase_sheep*self.weight_a) + (away_from_sheep*self.weight_b) + (away_from_goal*self.weight_c)
            
            
            
        """avoid impassable obstacles"""
        movement += (self.env.avoid_impassable_obstacles(self.pos, self.velocity) * 200)
        
        # print(f"movement: {movement}")
        
        if norm(movement) > 0:
            # print("movement change")
            # self.velocity = 0.9*self.velocity + 2*movement #TODO: is this weighting what we want?
            self.velocity = movement

        # print(self.velocity)


