import tkinter as tk
import numpy as np
from numpy import random

# basic boid class
class Boid:
    # position x,y
    pos = np.array([0,0])
    # acceleration x,y
    acceleration = np.array([0,0])
    # velocity x,y
    velocity = np.array([10,10])
    # speed = magnitude of velocity
    speed = np.linalg.norm(velocity)
    max_speed = 25

    boid_radius = 25

    def __init__(self, c) -> None:
        self.canvas = c
        self.c_width = c.winfo_width()
        self.c_height = c.winfo_height()
        # print(self.c_width, self.c_height)

        self.start_pos(self.c_width, self.c_height)
        self.draw_boid(self.pos, self.boid_radius)


    # random start position within starting area
    # xMax, yMax bounds of start area
    def start_pos(self, xMax, yMax):
        self.pos = np.array([random.rand()*xMax, random.rand()*yMax])
        # print(self.pos)

    def draw_boid(self, pos, rad):
        self.drawing = self.canvas.create_oval(pos[0]-rad,pos[1]-rad,pos[0]+rad,pos[1]+rad, fill="black")

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


    def move_boid(self):
        self.calc_velocity()

        self.canvas.move(self.drawing, self.velocity[0], self.velocity[1])

        (leftpos, toppos, rightpos, bottompos)=self.canvas.coords(self.drawing)
   
        if leftpos <=0 or rightpos>=self.c_width:
            self.velocity[0]=-self.velocity[0]

        if toppos <=0 or bottompos >=self.c_height:
            self.velocity[1]=-self.velocity[1]
        
        self.canvas.after(30, self.move_boid)




