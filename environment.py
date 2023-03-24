import numpy as np
from numpy import random
import math

class Environment:

    height : int = 0
    width : int = 0

    def __init__(self, h:int, w:int):
        self.height = h
        self.width = w

    def check_valid_position(self, p): # p : np.array
        if (p[0] in range(self.width)) and (p[1] in range(self.height)):
            return True
        else:
            return False