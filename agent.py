import tkinter as tk
import numpy as np
from numpy import random

# basic agent class
class Agent:
    # position x,y
    pos = np.array([0,0])
    
    # acceleration x,y
    acceleration = np.array([0.0,0.0])  # use for obstacle avoid??
    
    # velocity x,y
    velocity = np.array([10.0,10.0])

    next_velocity = np.array([10.0,10.0])
    
    # speed = magnitude of velocity
    speed = np.linalg.norm(velocity)
    # max_speed = math.sqrt(200)
    max_speed = 25

    #
    vision_range = 50

    # drawing vars
    shape_radius = 5
    fill_colour = "black"

    def __init__(self, id:int, h, w):
        self.id = id
        self.area_height = h
        self.area_width = w

    def set_pos(self, p): # p:np.array
        self.pos = p

    def get_pos(self): # -> np.array
        return self.pos

    # def draw_agent(self, pos, rad):
    #     self.drawing = self.canvas.create_oval(pos[0]-rad,pos[1]-rad,pos[0]+rad,pos[1]+rad, fill=self.fill_colour)

    def find_nearby(self, agents, dists): # dists : np.array[[]]
        # read in distance matrix and array of agents
        # use agent ID to pull correct row from dist matrix
        relevant_dists = dists[self.id]
        # apply filter to check for distances in vision_range
        nearby = relevant_dists <= self.vision_range
        nearby[self.id] = False
        # match indexes to IDs of other agents
        nearby_agents = agents[nearby]          # check this!!!!!
        # return array of nearby agents
        return nearby_agents

    def calc_acceleration(self):
        pass

    def calc_velocity(self):
        # v + a
        # keep new v under max spd
        self.velocity = np.add(self.velocity, self.acceleration)  # why does this line make everything work???
        self.speed = self.speed = np.linalg.norm(self.velocity)
        # if self.speed > self.max_speed:
            # print("yup")
        self.velocity[0] = (self.velocity[0] / self.speed) * self.max_speed
        self.velocity[1] = (self.velocity[1] / self.speed) * self.max_speed

        # print(self.velocity)

    def normalise_velocity(self):
        pass

    def update_velocity(self):
        self.velocity = self.next_velocity.copy()
        
    def update_agent(self):
        # self.calc_acceleration()
        self.calc_velocity()

        # check if next pos is valid
        bound_inset = 30
        xMin = bound_inset
        yMin = bound_inset
        xMax = self.area_width - bound_inset
        yMax = self.area_height - bound_inset

        edge_avoid_factor = 25

        if self.pos[0] < xMin:
            self.velocity[0] += edge_avoid_factor
            # self.velocity[0] = -self.velocity[0]
        elif self.pos[0] > xMax:
            self.velocity[0] -= edge_avoid_factor
            # self.velocity[0] = -self.velocity[0]

        if self.pos[1] < yMin:
            self.velocity[1] += edge_avoid_factor
            # self.velocity[1] = -self.velocity[1]
        elif self.pos[1] > yMax:
            self.velocity[1] -= edge_avoid_factor
            # self.velocity[1] = -self.velocity[1]

    
        # print(self.id, self.velocity)

        # update pos
        self.pos = self.pos + self.velocity







