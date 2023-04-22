import numpy as np
from numpy import random
import math
from math import sin, cos, tan, pi
from matplotlib import patches

class Obstacle:
    
    # coords (rectangle)
    pos = np.array([10,10]) # bottom left corner
    width = 10
    height = 5

    # nearby boundary
    near_range = 5

    # 0 = Fog; 1 = Mud; 2 = Hedge
    type = 0

    # effects
    passable = True
    reduce_movement = False
    reduce_vision = True
    block_vision = False
    colour = "grey"
    
    def __init__(self, id, t, p, w, h):
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
        s = "Obs id: {}, type: {}, pos: {}, size: {}x{}".format(self.id, t, self.pos, self.width, self.height)
        return s
    
    def draw(self):
        return patches.Rectangle((self.pos[0], self.pos[1]), self.width, self.height, linewidth=1, color=self.colour)

    def is_inside(self, p):
        if (p[0]>=self.pos[0] and p[0]<=self.pos[0]+self.width) and (p[1]>=self.pos[1] and p[1]<=self.pos[1]+self.height):
            return True
        else:
            return False

    def is_near(self, p, v):
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
        
        steer_away = np.array([0.0, 0.0])
        
        # use trig here to do these rotations, scale theta inv prop to dist from edge ranging 15(?) deg to 90 deg
        # ! should this ALSO be inversely proportional to the angle the agent is??
        # ! if an agent is close, but barely going to collide, does it really need to turn so sharply?
        theta = 15
        turn = np.array([0.0, 0.0])

        if p[0]>=self.pos[0]-self.near_range: # to right of x min
            collide_xmin, y_pred = calc_collision_in_x(p, v, self.pos[0], self.pos[1], self.pos[1]+self.height)
            
            # if will collide, scale steering 
            if collide_xmin == True:
                d = math.dist(p, [self.pos[0],y_pred])
                theta = ((1/d) * (90-15)) + 15 # dist between agent and [xmin, y_pred]
                
            # if grad +, rotate vel anticlockwise, +theta
            # redundant to include this part of the if
            # if grad -, rotate vel clockwise, -theta
            if v[1]/v[0] < 0:
                theta *= -1 

            print(f"theta: {theta}")
            turn = np.array([v[0]*cos(theta) - v[1]*sin(theta), v[0]*sin(theta) + v[1]*cos(theta)])     
        
        elif p[0]<=self.pos[0]+self.width+self.near_range: # to left of x max
            collide_xmax, y_pred = calc_collision_in_x(p, v, self.pos[0]+self.width, self.pos[1], self.pos[1]+self.height)
            
            # if will collide, scale steering 
            if collide_xmax == True:
                d = math.dist(p, [self.pos[0]+self.width,y_pred])
                theta = ((1/d) * (90-15)) + 15
                
            # if grad +, rotate vel clockwise, -theta
            if v[1]/v[0] >= 0:
                theta *= -1
            # if grad -, rotate vel anticlockwise, +theta
            # redundant to include this part of the if
            print(f"theta: {theta}")
            turn = np.array([v[0]*cos(theta) - v[1]*sin(theta), v[0]*sin(theta) + v[1]*cos(theta)]) 
        
        steer_away += turn # add turn
        turn = np.array([0.0, 0.0]) # reset turn
        theta = 15 # reset theta

        if p[1]>=self.pos[1]-self.near_range: # above y min
            collide_ymin, x_pred_ymin = calc_collision_in_y(p, v, self.pos[1], self.pos[0], self.pos[0]+self.width)
            
            if collide_ymin == True:
                d = math.dist(p, [x_pred,self.pos[1]])
                theta = ((1/d) * (90-15)) + 15
                
            # if grad +, rotate vel clockwise, -theta
            if v[1]/v[0] >= 0:
                theta *= -1
            # if grad -, rotate vel anticlockwise, +theta
            # redundant to include this part of the if
            print(f"theta: {theta}")
            turn = np.array([v[0]*cos(theta) - v[1]*sin(theta), v[0]*sin(theta) + v[1]*cos(theta)])
                
        
        elif p[1]<=self.pos[1]+self.height+self.near_range: # below y max
            collide_ymax, x_pred = calc_collision_in_y(p, v, self.pos[1]+self.height, self.pos[0], self.pos[0]+self.width)
            
            if collide_ymax == True:
                d = math.dist(p, x_pred, self.pos[1]+self.height)
                theta = ((1/d) * (90-15)) + 15
                
            # if grad +, rotate vel clockwise, -theta
            if v[1]/v[0] >= 0:
                theta *= -1
            # if grad -, rotate vel anticlockwise, +theta
            # redundant to include this part of the if
            print(f"theta: {theta}")
            turn = np.array([v[0]*cos(theta) - v[1]*sin(theta), v[0]*sin(theta) + v[1]*cos(theta)])
            
        steer_away += turn # add turn
        
        unit_steer_away = steer_away / np.linalg.norm(steer_away)
        return unit_steer_away

# helper function to check if is a collision path on left or right
#! these funcs dont inherantly account for being inside an obstacle
def calc_collision_in_x(pos, vel, x, ymin, ymax):
    grad = vel[1]/vel[0]
    c = pos[1] - (grad*pos[0])
    y_predict = (grad*x) + c
    
    if (ymin <= y_predict) and (y_predict <= ymax) and (((pos[0] <= x) and (vel[0] > 0)) or ((pos[0] >= x) and (vel[0] < 0))):
        return True, y_predict

    return False, y_predict

# helper function to check if is a collision path on top or bottom
def calc_collision_in_y(pos, vel, y, xmin, xmax):
    grad = vel[1]/vel[0]
    c = pos[1] - (grad*pos[0])
    x_predict = (y-c)/grad
    
    if (xmin <= x_predict) and (x_predict <= xmax) and (((pos[1] <= y) and (vel[1] > 0)) or ((pos[1] >= y) and (vel[1] < 0))):
        return True, x_predict

    return False, x_predict
