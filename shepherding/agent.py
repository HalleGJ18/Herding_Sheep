import tkinter as tk
import numpy as np
from numpy.linalg import norm
from numpy import random
import math

from shepherding.environment import Environment 

# basic agent class
class Agent:
    # position x,y
    pos = np.array([0,0])
    
    # acceleration x,y
    acceleration = np.array([0.0,0.0])  # use for obstacle avoid??
    
    # velocity x,y
    velocity = np.array([0.0,0.0])

    next_velocity = np.array([10.0,10.0])
    
    # speed = magnitude of velocity
    speed = norm(velocity)

    #
    default_max_speed = 1
    max_speed = 1 #5

    #
    default_vision_range = 2
    vision_range = 2

    # drawing vars
    fill_colour = "black"

    def __init__(self, id:int, e:Environment):
        self.id = id
        self.env = e
        self.area_height = e.height
        self.area_width = e.width

    def set_pos(self, p): # p:np.array
        self.pos = p

    def get_pos(self): # -> np.array
        return self.pos

    def find_nearby(self, agents, dists): # dists : np.array[[]]
        # read in distance matrix and array of agents
        # use agent ID to pull correct row from dist matrix
        relevant_dists = dists[self.id]
        # apply filter to check for distances in vision_range
        nearby = relevant_dists <= self.vision_range
        nearby[self.id] = False
        # match indexes to IDs of other agents
        nearby_agents = agents[nearby]          # check this!!!!!
        # check if blocked by obstacle
        if self.env.vision_obstructions:
            nearby_agents = np.array([a for a in nearby_agents if self.env.is_obstacle_blocking_vision(self.pos, a.pos) == False])
        # return array of nearby agents
        return nearby_agents

    def can_see(self, pos, range):
        # include env checks
        if math.dist(self.pos, pos) <= range:
            if not self.env.is_obstacle_blocking_vision(self.pos, pos):
                return True
        return False

    def rand_velocity(self):
        # lim = self.max_speed
        lim = 2
        half = 1
        x = random.randint(0,lim) - half + random.rand()
        y = random.randint(0,lim) - half + random.rand()
        v = np.array([x,y])
        v = v / norm(v)
        return v

    def calc_velocity(self):
        # v + a
        # keep new v under max spd
        self.velocity = np.add(self.velocity, self.acceleration)  # why does this line make everything work???
        self.speed = norm(self.velocity)
        if self.speed != 0: # > max_speed, cap it
            self.velocity = self.velocity / self.speed * self.max_speed
            self.speed = norm(self.velocity)


    def update_velocity(self):
        self.velocity = self.next_velocity.copy()
        
    def update_agent(self):
        self.calc_velocity()
        
        avoid = self.env.avoid_impassable_obstacles(self.pos, self.velocity) # ! tweaking this
        if norm(avoid) > 0:
            self.velocity += (avoid*1)
        
        self.calc_velocity()

        self.velocity += self.env.check_valid_position(self.pos, self.velocity)

        # update pos
        self.pos = self.pos + self.velocity







