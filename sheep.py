import tkinter as tk
import tkinter as tk
import numpy as np
from numpy import random
import math
from agent import Agent

class Sheep(Agent):

    personal_space = 30
    
    def separation(self, agents, dists):
        # find nearby agents
        nearby = self.find_nearby(agents, dists)

        # don't get too close to other agents nearby
        cumulative_vector = np.array([0,0])
        num_of_nearby = len(nearby)
        
        for a in agents:
            # find the average vector of the other agent to the current agent each multiplied by the inverse of the distance
            dist = math.dist(self.pos, a.pos)
            v = (1/dist)*(self.pos - a.pos)
            cumulative_vector += v

        sep_vector = cumulative_vector/num_of_nearby
        return sep_vector
        

    def alignment(self, agents, dists):
        # steer towards average heading
        # heading = pos + vel ??? make this a class var??
        
        pass

    def cohesion(self, agents, dists):
        # steer towards average position
        pass

    def calc_acceleration(self, agents, dists):
        self.separation(agents)
        pass
        # call the flocking funcs???