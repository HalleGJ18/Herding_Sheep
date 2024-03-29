import tkinter as tk
import numpy as np
from numpy.linalg import norm
from numpy import random
import math

from shepherding.agent import Agent

class Sheep(Agent):

    personal_space = 2 #2

    dog_in_range = False
    seen_dogs = 0
    total_dogs = 1

    velocity = np.array([0.1, 0.1])

    threat_range = 65 #45

    max_speed = 1 #1
    
    n_closest = 100
    
    default_vision_range = 40 #20
    vision_range = 40
    
    too_close = False
    

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
                d = d/norm(d)
                total_separation += d
                too_close += 1
            
            if too_close > 0:
                self.too_close = True
            else:
                self.too_close = False

            # alignment
            # match velocity of neighbours
            total_alignment += s.velocity

            # cohesion
            # steer towards average position
            total_cohesion += (s.pos - self.pos)

        if too_close > 0:
            sep_vector = (total_separation/too_close)
        else:
            sep_vector = total_separation
        
        if norm(sep_vector) != 0:
            sep_vector = sep_vector/norm(sep_vector)


        align_vector = (total_alignment/len(nearby)) - self.velocity
        if norm(align_vector) != 0:
            align_vector = align_vector/norm(align_vector)


        cohes_vector = (total_cohesion/len(nearby)) # - self.pos
        if norm(cohes_vector) != 0:
            cohes_vector = cohes_vector/norm(cohes_vector)

        # print(self.id, sep_vector, align_vector, cohes_vector)

        return sep_vector, align_vector, cohes_vector


    def apply_flocking(self, agents, dists, sep_weight, align_weight, cohes_weight, dog_push_weight):

        noise_weight = 0.3
        prev_vel_weight = 0.5

        velocity_changes = np.array([0.0, 0.0])
        
        """avoid sheepdogs"""
        # nearby sheepdogs
        if self.dog_in_range:

            # get unit vector away from dog avg pos
            # away = self.dog_in_range_avg / norm(self.dog_in_range_avg) # TODO: scale this by dogs_in_range/n_dogs
            away = self.pos - self.dog_in_range_avg
            away = away/norm(away)
            # print(f"away: {away}")
            velocity_changes += (away*dog_push_weight) #*(self.seen_dogs/self.total_dogs)

            # print("dog near")
            # print(away*dog_push_weight)
        

        """flocking"""

        nearby_sheep = self.find_nearby(agents, dists)
        
        # n nearest neighbours
        # sort by dist and keep n closest
        sorted_by_dist = sorted(nearby_sheep, key= lambda sheep: math.dist(sheep.pos, self.pos))
        if len(sorted_by_dist) > self.n_closest:
            nearby_sheep = sorted_by_dist[:self.n_closest]
        else:
            nearby_sheep = sorted_by_dist
        
        # call the flocking funcs???
        if len(nearby_sheep) > 0:
            separation, alignment, cohesion =  self.flocking_algo(nearby_sheep)
            
            if self.dog_in_range:
                # velocity_changes = velocity_changes + sep_weight*separation + align_weight*alignment + cohes_weight*cohesion 
                velocity_changes = velocity_changes + sep_weight*separation + cohes_weight*cohesion 
            else:
                velocity_changes = velocity_changes + (sep_weight*separation)
                
        else:
            self.too_close = False


        noise = self.rand_velocity()

        if (self.dog_in_range == False) : # and (len(nearby_sheep) == 0) 
            if self.too_close:
                # seperation regardless of sheepdog vicinity
                self.velocity = self.velocity*prev_vel_weight + velocity_changes
            else:
                rand_chance = np.random.rand()
                if rand_chance <= 0.05: # random chance of slight movement
                    self.velocity = noise
                else:
                    self.velocity = np.array([0.0, 0.0])
        else:
            
            velocity_changes = velocity_changes + (noise_weight * noise)
            self.velocity = self.velocity*prev_vel_weight + velocity_changes
            # self.velocity += velocity_changes