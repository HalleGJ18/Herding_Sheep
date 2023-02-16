import tkinter as tk
import tkinter as tk
import numpy as np
from numpy import random
import math
from agent import Agent

class Sheep(Agent):
    
    def separation(self, agents):
        # don't get too close to other agents nearby
        # find the average vector of the other agent to the current agent each multiplied by the inverse of the distance
        personal_space = 30
        cumulative_vector = np.array([0,0])
        nearby_agents = 0
        for b in agents:
            dist = math.dist(self.pos, b.pos)
            if dist < personal_space and (b is not self):
                v = (1/dist)*(self.pos - b.pos)
                cumulative_vector += v
                nearby_agents += 1
        # sep_vector = 
        

    def alignment(self, agents):
        # steer towards average heading
        # heading = pos + vel ??? make this a class var??

        pass

    def cohesion(self, agents):
        # steer towards average position
        pass

    def calc_acceleration(self):
        pass
    # call the flocking funcs???