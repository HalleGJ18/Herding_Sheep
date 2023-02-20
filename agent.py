import tkinter as tk
import numpy as np
from numpy import random
import math

# basic agent class
class Agent:
    # position x,y
    pos = np.array([0,0])
    
    # acceleration x,y
    acceleration = np.array([0,0])
    
    # velocity x,y
    velocity = np.array([10,10])
    
    # speed = magnitude of velocity
    speed = np.linalg.norm(velocity)
    max_speed = 25

    #
    vision_range = 50

    # drawing vars
    shape_radius = 25
    fill_colour = "black"

    def __init__(self, id, c) -> None:
        self.id = id
        self.canvas = c
        self.c_width = c.winfo_width()
        self.c_height = c.winfo_height()

        self.start_pos(25, 25, self.c_width-25, self.c_height-25)
        # create changable vars for start pos range
        # will need to be different for sheep vs sheepdogs

        self.draw_agent(self.pos, self.shape_radius)


    # random start position within starting area
    # xMin, yMin, xMax, yMax bounds of start area
    def start_pos(self, xMin, yMin, xMax, yMax):
        xDiff = xMax-xMin
        yDiff = yMax-yMin
        self.pos = np.array([random.rand()*xDiff + xMin, random.rand()*yDiff + yMin])
        # print(self.pos)

    def draw_agent(self, pos, rad):
        self.drawing = self.canvas.create_oval(pos[0]-rad,pos[1]-rad,pos[0]+rad,pos[1]+rad, fill=self.fill_colour)

    def find_nearby(self, agents, dists):
        # read in distance matrix and array of agents
        # use agent ID to pull correct row from dist matrix
        relevant_dists = dists[self.id]
        # apply filter to check for distances in vision_range
        nearby = relevant_dists <= self.vision_range
        nearby[self.id] = False
        print(nearby)
        # match indexes to IDs of other agents
        nearby_agents = agents[nearby]
        # return array of nearby agents
        return nearby_agents

    def calc_acceleration(self):
        pass
    # call the flocking funcs???

    def calc_velocity(self):
        # v + a
        # keep new v under max spd
        self.velocity = np.add(self.velocity, self.acceleration)
        if self.speed > self.max_speed:
            self.velocity[0] = (self.velocity[0] / self.speed) * self.max_speed
            self.velocity[1] = (self.velocity[1] / self.speed) * self.max_speed

        # print(self.velocity)


    def move_agent(self):
        # calc acceleration
        # self.calc_acceleration()
        self.calc_velocity()

        self.canvas.move(self.drawing, self.velocity[0], self.velocity[1])
        self.pos = self.pos + self.velocity

        (leftpos, toppos, rightpos, bottompos)=self.canvas.coords(self.drawing)
   
        if leftpos <=0 or rightpos>=self.c_width:
            self.velocity[0]=-self.velocity[0]

        if toppos <=0 or bottompos >=self.c_height:
            self.velocity[1]=-self.velocity[1]
        
        # self.canvas.after(30, self.move_agent)




