import tkinter as tk
import numpy as np
from numpy import random
import math

from agent import Agent

class Sheep(Agent):

    personal_space = 30

    dog_in_range = False
    
    # def separation(self, sheep):
    #     # don't get too close to other agents nearby
    #     cumulative_vector = np.array([0.0,0.0])
        
    #     for a in sheep:
    #         # find the average vector of the other agent to the current agent each multiplied by the inverse of the distance
    #         dist = math.dist(self.pos, a.pos)
    #         v = (1/dist)*(self.pos - a.pos)
    #         cumulative_vector += v

    #     sep_vector = cumulative_vector/len(sheep)
        
    #     return sep_vector
        

    # def alignment(self, sheep):
    #     # match velocity
    #     cumulative_vector = np.array([0.0,0.0])

    #     for s in sheep:
    #         cumulative_vector += s.velocity

    #     # how far from avg velocity are we?
    #     align_vector = (cumulative_vector/len(sheep)) - self.velocity
        
    #     return align_vector
            

    # def cohesion(self, sheep):
    #     # steer towards average position

    #     cumulative_vector = np.array([0.0,0.0])
        
    #     for s in sheep:
    #         cumulative_vector += s.pos

    #     cohes_vector = (cumulative_vector/len(sheep)) - self.pos

    #     return cohes_vector

    def set_avg_dog_pos(self, p):
        self.dog_in_range_avg = p
    

    def flocking_algo(self, nearby):
        total_separation = np.array([0.0,0.0])
        total_alignment = np.array([0.0,0.0])
        total_cohesion = np.array([0.0,0.0])

        for s in nearby:
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

        if np.linalg.norm(total_separation) > 0:
            sep_vector = (total_separation/len(nearby))
        else:
            sep_vector = total_separation

        align_vector = (total_alignment/len(nearby)) - self.velocity
        cohes_vector = (total_cohesion/len(nearby)) - self.pos

        # print(self.id, sep_vector, align_vector, cohes_vector)

        return sep_vector, align_vector, cohes_vector


    def apply_flocking(self, agents, dists, sep_weight, align_weight, cohes_weight, dog_push_weight):

        velocity_changes = np.array([0.0, 0.0])
        
        # nearby sheepdogs
        if self.dog_in_range:
            # get unit vector away from dog avg pos
            away = self.dog_in_range_avg / np.linalg.norm(self.dog_in_range_avg)
            # away = self.dog_in_range_avg

            velocity_changes += (away*dog_push_weight)

            # print("dog near")
            # print(away*dog_push_weight)

        # else:
        #     velocity_changes = np.array([0.0, 0.0])
        
        
        nearby_sheep = self.find_nearby(agents, dists)
        
        # call the flocking funcs???
        if len(nearby_sheep) > 0:
            separation, alignment, cohesion =  self.flocking_algo(nearby_sheep)
            # self.velocity = 5*random.uniform(-1,2,(2)) + sep_weight*separation + align_weight*alignment + cohes_weight*cohesion
            self.velocity = self.velocity + sep_weight*separation + align_weight*alignment + cohes_weight*cohesion + velocity_changes
            # self.velocity = self.velocity + separation + alignment + cohesion 
        else:
            self.velocity = 0.7*self.velocity + 5*random.uniform(-1,2,(2)) + velocity_changes

        # self.calc_velocity()      # what is this doing here?

