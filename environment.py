import numpy as np
from numpy import random
import math

class Environment:

    height : int = 0
    width : int = 0

    bound_inset = 15 #! scale with env size

    edge_avoid_factor = 25 #! scale with env size

    def __init__(self, h:int, w:int):
        self.height = h
        self.width = w

    def check_valid_position(self, p): # p : np.array
        if (p[0] in range(self.width)) and (p[1] in range(self.height)):
            return True
        else:
            return False
        
    def init_obstacles(self):
        pass

    def draw_obstacles(self):
        pass