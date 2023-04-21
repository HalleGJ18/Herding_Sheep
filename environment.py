import numpy as np
from numpy import random
import math
from obstacle import Obstacle

class Environment:

    height : int = 0
    width : int = 0

    obstacles = []

    bound_inset = 15 #! scale with env size
    edge_avoid_factor = bound_inset + 5 #! scale with env size

    def __init__(self, h:int, w:int):
        self.height = h
        self.width = w

        self.xMin = self.bound_inset
        self.yMin = self.bound_inset
        self.xMax = self.width - self.bound_inset
        self.yMax = self.height - self.bound_inset

        self.init_obstacles()

    def init_obstacles(self):
        self.obstacles.append(Obstacle(0, 2, [250,250], 10, 5))

        for o in self.obstacles:
            print(o.to_string())

    def check_valid_position(self, p): # p : np.array

        avoid_amount = np.array([0,0])

        # if not inside outer boundary
        if not ((p[0] in range(self.width)) and (p[1] in range(self.height))):
            # return velocity change needed to turn away
            

            if p[0] < self.xMin:
                avoid_amount[0] += self.edge_avoid_factor
            elif p[0] > self.xMax:
                avoid_amount[0] -= self.edge_avoid_factor

            if p[1] < self.yMin:
                avoid_amount[1] += self.edge_avoid_factor
            elif p[1] > self.yMax:
                avoid_amount[1] -= self.edge_avoid_factor

        # check obstacles


        # return avoid amount
        if avoid_amount[0] != 0 or avoid_amount[1] != 0:
            print(avoid_amount)

        return avoid_amount

    def check_pos_against_obstacles(self, p):
        if len(self.obstacles) > 0:
            for o in self.obstacles:
                if o.passable == False:
                    if o.is_inside(p):
                        pass
                        # move away
                    else:
                        # if near?
                        pass

    def draw_obstacles(self):
        pass