import numpy as np
from numpy import random
import math
from agent import Agent

class Sheepdog(Agent):

    target = np.array([600.0, 600.0])

    vision_range = 300 # increase?

    # calc line from target to flock com

    # calc most direct vector to line
