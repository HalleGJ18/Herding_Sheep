import tkinter as tk
import numpy as np
from numpy import random
import math

from agent import Agent

class Sheep(Agent):

    personal_space = 5 #2

    dog_in_range = False

    velocity = np.array([0.1, 0.1])

    threat_range = 65

    max_speed = 5 #1
    
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
            too_close = 0
            if dist <= self.personal_space:
                d = self.pos - s.pos
                d = d/np.linalg.norm(d)
                total_separation += d
                too_close += 1

            # alignment
            # match velocity of neighbours
            total_alignment += s.velocity

            # cohesion
            # steer towards average position
            total_cohesion += s.pos

        if too_close > 0:
            sep_vector = (total_separation/too_close)
        else:
            sep_vector = total_separation
        
        if np.linalg.norm(sep_vector) != 0:
            sep_vector = sep_vector/np.linalg.norm(sep_vector)


        align_vector = (total_alignment/len(nearby)) - self.velocity
        if np.linalg.norm(align_vector) != 0:
            align_vector = align_vector/np.linalg.norm(align_vector)


        cohes_vector = (total_cohesion/len(nearby)) - self.pos
        if np.linalg.norm(cohes_vector) != 0:
            cohes_vector = cohes_vector/np.linalg.norm(cohes_vector)

        # print(self.id, sep_vector, align_vector, cohes_vector)

        # check vector lengths

        # print(np.linalg.norm(sep_vector), np.linalg.norm(align_vector), np.linalg.norm(cohes_vector))
        # p = ""
        # if np.linalg.norm(sep_vector) != 0:
        #     p = p + "sep: {}".format(np.linalg.norm(sep_vector))
        # if np.linalg.norm(align_vector) != 0:
        #     p = p + " ali: {}".format(np.linalg.norm(align_vector))
        # if np.linalg.norm(cohes_vector) != 0:
        #     p = p + " coh: {}".format(np.linalg.norm(cohes_vector))
        # if p != "":
        #     print(p)

        return sep_vector, align_vector, cohes_vector


    def apply_flocking(self, agents, dists, sep_weight, align_weight, cohes_weight, dog_push_weight):

        noise_weight = 0.3
        prev_vel_weight = 0.5

        velocity_changes = np.array([0.0, 0.0])
        
        """avoid sheepdogs"""
        # nearby sheepdogs
        if self.dog_in_range:

            # get unit vector away from dog avg pos
            away = self.dog_in_range_avg / np.linalg.norm(self.dog_in_range_avg)

            velocity_changes += (away*dog_push_weight)

            # print("dog near")
            # print(away*dog_push_weight)
        


        """flocking"""

        nearby_sheep = self.find_nearby(agents, dists)
        
        # call the flocking funcs???
        if len(nearby_sheep) > 0:
            separation, alignment, cohesion =  self.flocking_algo(nearby_sheep)
            
            # velocity_changes = velocity_changes + sep_weight*separation + align_weight*alignment + cohes_weight*cohesion 
            
            if self.dog_in_range:
                velocity_changes = velocity_changes + sep_weight*separation + align_weight*alignment + cohes_weight*cohesion 
                # velocity_changes = velocity_changes + sep_weight*separation + cohes_weight*cohesion 
            else:
                # print("sep: {}".format(separation*sep_weight))
                velocity_changes = velocity_changes + (sep_weight*separation)

        # self.calc_velocity()      # what is this doing here?

        noise = self.rand_velocity()

        if (self.dog_in_range == False) and (len(nearby_sheep) == 0):
            rand_chance = np.random.rand()
            if rand_chance <= 0.05: # random chance of slight movement
                # print("rand move, {}".format(self.id))
                # print(noise)
                self.velocity = noise
            else:
                self.velocity = np.array([0.0, 0.0])
        elif (self.dog_in_range == False) and (len(nearby_sheep) > 0):
            self.velocity = velocity_changes
            # print(velocity_changes)
        else:
            
            velocity_changes = velocity_changes + (noise_weight * noise)
            self.velocity = self.velocity*prev_vel_weight + velocity_changes
            # self.velocity += velocity_changes

        # print("vel: {}".format(self.velocity))
