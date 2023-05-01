import numpy as np
from numpy import random
import math
from obstacle import Obstacle

class Environment:

    height : int = 0
    width : int = 0
    
    target = np.array([125.0, 25.0])
    target_range = 10
    target_endzone = 25 #25

    obstacles = []
    
    speed_reduction_factor = 0.75
    vision_reduction_factor = 0.75
    

    bound_inset = 5 #! scale with env size
    edge_avoid_factor = 3 #! scale with env size

    def __init__(self, h:int, w:int):
        self.height = h
        self.width = w

        self.xMin = self.bound_inset
        self.yMin = self.bound_inset
        self.xMax = self.width - self.bound_inset
        self.yMax = self.height - self.bound_inset

        # self.init_obstacles()

    def init_obstacles(self):
        self.obstacles.append(Obstacle(0, 2, [100,150], 100, 30))
        self.obstacles.append(Obstacle(1, 0, [100,500], 75, 100))
        self.obstacles.append(Obstacle(2, 1, [500,100], 50, 50))
        self.obstacles.append(Obstacle(3, 1, [300,300], 100, 50))

        for o in self.obstacles:
            print(o.to_string())

    def check_valid_position(self, p, v): # p : np.array    v : np.array

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

        
        # if avoid_amount[0] != 0 or avoid_amount[1] != 0:
        #     print(avoid_amount)

        # return avoid amount
        return avoid_amount
    
    def check_all_obstacles(self, p):
        ok = True
        if len(self.obstacles) > 0:
            for o in self.obstacles:
                if o.is_inside(p):
                    ok = False
                    break
        return ok

    def avoid_impassable_obstacles(self, p, v):
        turn = np.array([0.0, 0.0])
        if len(self.obstacles) > 0:
            o:Obstacle
            for o in self.obstacles:
                if o.passable == False:
                    # print(f"avoid: {o.id}, {o.colour}")
                    turn += o.avoid(p,v) # will be [0,0] if not nearby
        # print(f"turn: {turn}")
        return turn
                        
    def line_rect_intersect(self, line, rect):
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
        corner, width, height = rect
        x_min, y_min = corner

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
    
    def is_obstacle_blocking_vision(self, pos1, pos2):
        obstacle: Obstacle
        if len(self.obstacles) > 0:
            for obstacle in self.obstacles:
                if obstacle.block_vision:
                    if obstacle.line_rect_intersect([pos1,pos2]):
                        return True
        return False
    
    def is_obstacle_reducing_movement(self, p):
        obstacle:Obstacle
        if len(self.obstacles) > 0:
            for obstacle in self.obstacles:
                if obstacle.reduce_movement:
                    if obstacle.is_inside(p):
                        return True
        return False
    
    def is_obstacle_reducing_vision(self, p):
        obstacle:Obstacle
        if len(self.obstacles) > 0:
            for obstacle in self.obstacles:
                if obstacle.reduce_vision:
                    if obstacle.is_inside(p):
                        return True
        return False
    
    def in_endzone(self, p):
        x_inside = False
        y_inside = False
        # check x in range
        if (p[0] >= self.target[0]-self.target_endzone) and (p[0] <= self.target[0]+self.target_endzone):
            x_inside = True
        # check y in range
        if (p[1] >= self.target[1]-self.target_endzone) and (p[1] <= self.target[1]+self.target_endzone):
            y_inside = True
        if x_inside and y_inside:
            return True
        else:
            return False