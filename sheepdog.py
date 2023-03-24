import numpy as np
from numpy import random

from agent import Agent

class Sheepdog(Agent):

    vision_range = 300 # increase?


    def set_target(self, t):
        # ingest np array
        # set target
        self.target = t

    def get_target(self):
        # return np array
        return self.target

    # calc line from target to flock centre of mass
    # find point on line where all sheep are closer to target than it
    # or, maintaining some distance from flock
    # calc most direct vector to point
    # average position of all sheepdogs should be this point
