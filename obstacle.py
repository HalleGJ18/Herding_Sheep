import numpy as np
from numpy import random
from numpy import arcsin, arccos, arctan, sin, cos, tan, pi
import math
# from math import sin, cos, tan, pi
from matplotlib import patches

class Obstacle:
    
    # coords (rectangle)
    pos = np.array([10,10]) # bottom left corner
    width = 10
    height = 5

    # nearby boundary
    near_range = 25
    
    avoid_strength = 2

    # 0 = Fog; 1 = Mud; 2 = Hedge
    type = 0

    # effects
    passable = True
    reduce_movement = False
    reduce_vision = True
    block_vision = False
    colour = "grey"
    
    def __init__(self, id, t, p, w, h):
        # id is obs id, manually increment
        # t is obs type (0,1,2)
        # p is bottom left corner
        # w is width
        # h is height
        self.id = id
        self.type = t
        self.pos = np.array(p)
        self.height = h
        self.width = w

        # default t == 0 is Fog
        if t == 1:
            # Mud
            self.passable = True
            self.reduce_movement = True
            self.reduce_vision = False
            self.block_vision = False
            self.colour = "saddlebrown"
        elif t == 2:
            # Hedge
            self.passable = False
            self.reduce_movement = False
            self.reduce_vision = False
            self.block_vision = True
            self.colour = "green"
        
    def to_string(self):
        t = ""
        if self.type == 0:
            t = "Fog"
        elif self.type == 1:
            t = "Mud"
        elif self.type == 2:
            t = "Hedge"
        s = f"Obs id: {self.id}, type: {t}, passable: {self.passable}, pos: {self.pos}, size: {self.width}x{self.height}"
        return s
    
    def export(self):
        return self.pos[0], self.pos[1], self.width, self.height, self.colour
    
    def draw(self):
        return patches.Rectangle((self.pos[0], self.pos[1]), self.width, self.height, linewidth=1, color=self.colour)

    def is_inside(self, p):
        if (p[0]>=self.pos[0] and p[0]<=self.pos[0]+self.width) and (p[1]>=self.pos[1] and p[1]<=self.pos[1]+self.height):
            return True
        else:
            return False
        
    def is_near(self,p):
        if (p[0]>=self.pos[0]-self.near_range and p[0]<=self.pos[0]+self.width+self.near_range) and (p[1]>=self.pos[1]-self.near_range and p[1]<=self.pos[1]+self.height+self.near_range):
            return True
        else:
            return False
        
    def line_rect_intersect(self, line):
        """
        Checks if a line intersects with a rectangle.

        Parameters:
        line (tuple): A tuple of two points representing the line.
        rect (tuple): A tuple of two floats representing the bottom-left corner of the rectangle, and two floats representing the width and height of the rectangle.

        Returns:
        bool: True if the line intersects with the rectangle, False otherwise.
        """
        x1, y1 = line[0]
        x2, y2 = line[1]
        corner = self.pos
        x_min, y_min = corner
        width = self.width 
        height = self.height
        

        # Calculate the values of p and q for the line
        dx = x2 - x1
        dy = y2 - y1
        p = [-dx, dx, -dy, dy]
        q = [x1 - x_min, x_min + width - x1, y1 - y_min, y_min + height - y1]

        # Initialize the values of u1 and u2 to be 0 and 1, respectively
        u1 = 0
        u2 = 1

        # Clip the line against each edge of the rectangle
        for i in range(4):
            if p[i] == 0:
                if q[i] < 0:
                    # Line is parallel to the edge and outside the rectangle
                    return False
            else:
                r = q[i] / p[i]
                if p[i] < 0:
                    if r > u2:
                        # Line is outside the rectangle
                        return False
                    elif r > u1:
                        u1 = r
                elif p[i] > 0:
                    if r < u1:
                        # Line is outside the rectangle
                        return False
                    elif r < u2:
                        u2 = r

        # Check if the clipped line intersects the rectangle
        if u1 > 0 or u2 < 1:
            x1_clip = x1 + u1 * dx
            y1_clip = y1 + u1 * dy
            x2_clip = x1 + u2 * dx
            y2_clip = y1 + u2 * dy
            if (x_min <= x1_clip <= x_min + width or x_min <= x2_clip <= x_min + width) and \
                    (y_min <= y1_clip <= y_min + height or y_min <= y2_clip <= y_min + height):
                return True

        return False

    def avoid(self, p, v):
        """if agent is near obstacle, checks if is on collision course
            if on collision course, calculate the turn the agent needs to make inversely proportional to distance from obstacle

        Args:
            p (list[float]): pos of agent
            v (list[float]): velocity of agent

        Returns:
            list[float]: turn as a unit vector
        """
        
        # assume already know not inside?

        collide_xmin = False
        collide_xmax = False
        collide_ymin = False
        collide_ymax = False
        
        turn = np.array([0.0, 0.0])
        
        if self.is_near(p):
        
            # use trig here to do these rotations, scale theta inv prop to dist from edge ranging 15(?) deg to 90 deg
            # ! should this ALSO be inversely proportional to the angle the agent is??
            # ! if an agent is close, but barely going to collide, does it really need to turn so sharply?

            if p[0]>=self.pos[0]-self.near_range: # to right of x min
                # print("approach x min")
                collide_xmin, y_pred = calc_collision_in_x(p, v, self.pos[0], self.pos[1], self.pos[1]+self.height)
                
                # if will collide, scale steering 
                if collide_xmin == True:
                    x_diff = self.pos[0]-p[0]
                    turn[0] -= x_diff   
            
            elif p[0]<=self.pos[0]+self.width+self.near_range: # to left of x max
                # print("approach x max")
                collide_xmax, y_pred = calc_collision_in_x(p, v, self.pos[0]+self.width, self.pos[1], self.pos[1]+self.height)
                
                # if will collide, scale steering 
                if collide_xmax == True:
                    x_diff = p[0]-(self.pos[0]+self.width)
                    turn[0] += x_diff


            if p[1]>=self.pos[1]-self.near_range: # above y min
                # print("approach y min")
                collide_ymin, x_pred = calc_collision_in_y(p, v, self.pos[1], self.pos[0], self.pos[0]+self.width)
                
                if collide_ymin == True:
                    y_diff = self.pos[1]-p[1]
                    turn[1] -= y_diff
                    
            
            elif p[1]<=self.pos[1]+self.height+self.near_range: # below y max
                # print("approach y max")
                collide_ymax, x_pred = calc_collision_in_y(p, v, self.pos[1]+self.height, self.pos[0], self.pos[0]+self.width)
                
                if collide_ymax == True:
                    y_diff = p[1]-(self.pos[1]+self.height)
                    turn[1] += y_diff
            
            # steer_away = steer_away / norm(steer_away)
        turn *= self.avoid_strength
        return turn

# helper function to check if is a collision path on left or right
#! these funcs dont inherantly account for being inside an obstacle
def calc_collision_in_x(pos, vel, x, ymin, ymax):
    
    # if little x velocity
    # either moving vertically or standing still
    if math.isclose(vel[0], 0, abs_tol=0.0001):
        return False, None
    # if little y velocity
    # only moving in x axis
    elif math.isclose(vel[1], 0, abs_tol=0.0001):
        y_predict = pos[1]  
    else:
        # grad = (vel[1]*10000)/(vel[0]*10000)
        grad = np.divide(vel[1], vel[0])
        c = pos[1] - (grad*pos[0])
        y_predict = (grad*x) + c
    
    if (ymin <= y_predict) and (y_predict <= ymax) and (((pos[0] <= x) and (vel[0] > 0)) or ((pos[0] >= x) and (vel[0] < 0))):
        return True, y_predict

    return False, y_predict

# helper function to check if is a collision path on top or bottom
def calc_collision_in_y(pos, vel, y, xmin, xmax):
    y_pred = None
    
    # if little y velocity
    # either moving horizontally or standing still
    if math.isclose(vel[1], 0, abs_tol=0.0001):
        return False, None
    # if little x velocity
    # only moving in y axis
    elif math.isclose(vel[0], 0, abs_tol=0.0001):
        x_predict = pos[0]
    else:
        # grad = (vel[1]*10000)/(vel[0]*10000)
        grad = np.divide(vel[1], vel[0])
        c = pos[1] - (grad*pos[0])
        x_predict = (y-c)/grad
    
    if (xmin <= x_predict) and (x_predict <= xmax) and (((pos[1] <= y) and (vel[1] > 0)) or ((pos[1] >= y) and (vel[1] < 0))):
        return True, x_predict

    return False, x_predict
