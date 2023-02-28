import tkinter as tk
import tkinter as tk
import numpy as np
from numpy import random
import math
from agent import Agent

class Sheep(Agent):

    personal_space = 30
    
    def separation(self, sheep):
        # don't get too close to other agents nearby
        cumulative_vector = np.array([0.0,0.0])
        
        for a in sheep:
            # find the average vector of the other agent to the current agent each multiplied by the inverse of the distance
            dist = math.dist(self.pos, a.pos)
            v = (1/dist)*(self.pos - a.pos)
            cumulative_vector += v

        sep_vector = cumulative_vector/len(sheep)
        
        return sep_vector
        

    def alignment(self, sheep):
        # match velocity
        cumulative_vector = np.array([0.0,0.0])

        for s in sheep:
            cumulative_vector += s.velocity

        # how far from avg velocity are we?
        align_vector = (cumulative_vector/len(sheep)) - self.velocity
        
        return align_vector
            

    def cohesion(self, sheep):
        # steer towards average position

        cumulative_vector = np.array([0.0,0.0])
        
        for s in sheep:
            cumulative_vector += s.pos

        cohes_vector = (cumulative_vector/len(sheep)) - self.pos

        return cohes_vector
    

    def flocking_algo(self, sheep):
        total_separation = np.array([0.0,0.0])
        total_alignment = np.array([0.0,0.0])
        total_cohesion = np.array([0.0,0.0])

        for s in sheep:
            # separation
            # don't get too close to neighbours
            dist = math.dist(self.pos, s.pos)
            # d = (1/dist)*(self.pos - s.pos)  # moderated by inverse of distance
            if dist < self.personal_space:
                d = self.pos - s.pos
                total_separation += d

            # alignment
            # match velocity of neighbours
            total_alignment += s.velocity

            # cohesion
            # steer towards average position
            total_cohesion += s.pos

        sep_vector = (total_separation/len(sheep)) - self.pos
        align_vector = (total_alignment/len(sheep)) - self.velocity
        cohes_vector = (total_cohesion/len(sheep)) - self.pos

        return sep_vector, align_vector, cohes_vector


    def apply_flocking(self, agents, dists, sep_weight, align_weight, cohes_weight):
        nearby_sheep = self.find_nearby(agents, dists)
        
        # call the flocking funcs???
        if len(nearby_sheep) > 0:
            separation, alignment, cohesion =  self.flocking_algo(nearby_sheep)
            # self.velocity = sep_weight*separation + align_weight*alignment + cohes_weight*cohesion
            self.velocity = self.velocity + separation + alignment + cohesion

        self.calc_velocity()

