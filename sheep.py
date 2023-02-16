import tkinter as tk
import tkinter as tk
import numpy as np
from numpy import random
import math
from agent import Agent

class Sheep(Agent):

    personal_space = 30
    
    def separation(self, agents):
        # find nearby agents
        nearby = []

        # use filter function to find agents closer than personal space ??
        # pass in dist matrix ???


        # don't get too close to other agents nearby
        # find the average vector of the other agent to the current agent each multiplied by the inverse of the distance
        cumulative_vector = np.array([0,0])
        nearby_agents = 0
        for a in agents:
            dist = math.dist(self.pos, a.pos)
            if dist < self.personal_space and (a is not self):
                v = (1/dist)*(self.pos - a.pos)
                cumulative_vector += v
                nearby_agents += 1
        sep_vector = cumulative_vector/nearby_agents
        return sep_vector
        

    def alignment(self, agents):
        # steer towards average heading
        # heading = pos + vel ??? make this a class var??

        pass

    def cohesion(self, agents):
        # steer towards average position
        pass

    def calc_acceleration(self, agents):
        self.separation(agents)
        pass
        # call the flocking funcs???