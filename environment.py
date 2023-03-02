import numpy as np
from numpy import random
import math

class Environment:

    height = 0
    width = 0

    def __init__(self, h, w):
        self.height = h
        self.width = w

    def check_valid_position(self, p):
        if (p[0] in range(self.width)) and (p[1] in range(self.height)):
            return True
        else:
            return False