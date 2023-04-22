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
        
        steer_away = np.array([0.0, 0.0])
        
        if self.is_near(p):
        
            # use trig here to do these rotations, scale theta inv prop to dist from edge ranging 15(?) deg to 90 deg
            # ! should this ALSO be inversely proportional to the angle the agent is??
            # ! if an agent is close, but barely going to collide, does it really need to turn so sharply?
            theta = 15
            turn = np.array([0.0, 0.0])

            if p[0]>=self.pos[0]-self.near_range: # to right of x min
                print("approach x min")
                collide_xmin, y_pred = calc_collision_in_x(p, v, self.pos[0], self.pos[1], self.pos[1]+self.height)
                
                # if will collide, scale steering 
                if collide_xmin == True:
                    d = math.dist(p, [self.pos[0],y_pred])
                    theta = ((1/d) * (90-15)) + 15 # dist between agent and [xmin, y_pred]
                    
                # if grad +, rotate vel anticlockwise, +theta
                # redundant to include this part of the if
                # if grad -, rotate vel clockwise, -theta
                if v[1] < 0: # y going down
                    theta *= -1 

                # print(f"theta: {theta}")
                turn = np.array([v[0]*cos(theta) - v[1]*sin(theta), v[0]*sin(theta) + v[1]*cos(theta)])     
            
            elif p[0]<=self.pos[0]+self.width+self.near_range: # to left of x max
                print("approach x max")
                collide_xmax, y_pred = calc_collision_in_x(p, v, self.pos[0]+self.width, self.pos[1], self.pos[1]+self.height)
                
                # if will collide, scale steering 
                if collide_xmax == True:
                    d = math.dist(p, [self.pos[0]+self.width,y_pred])
                    theta = ((1/d) * (90-15)) + 15
                    
                # if grad +, rotate vel clockwise, -theta
                if v[1] >= 0: # y going up
                    theta *= -1
                # if grad -, rotate vel anticlockwise, +theta
                # redundant to include this part of the if
                # print(f"theta: {theta}")
                turn = np.array([v[0]*cos(theta) - v[1]*sin(theta), v[0]*sin(theta) + v[1]*cos(theta)]) 
            
            steer_away += turn # add turn
            turn = np.array([0.0, 0.0]) # reset turn
            theta = 15 # reset theta

            if p[1]>=self.pos[1]-self.near_range: # above y min
                print("approach y min")
                collide_ymin, x_pred = calc_collision_in_y(p, v, self.pos[1], self.pos[0], self.pos[0]+self.width)
                
                if collide_ymin == True:
                    d = math.dist(p, [x_pred,self.pos[1]])
                    theta = ((1/d) * (90-15)) + 15
                    
                # if grad +, rotate vel clockwise, -theta
                if v[0] >= 0: # x going up
                    theta *= -1
                # if grad -, rotate vel anticlockwise, +theta
                # redundant to include this part of the if
                # print(f"theta: {theta}")
                turn = np.array([v[0]*cos(theta) - v[1]*sin(theta), v[0]*sin(theta) + v[1]*cos(theta)])
                    
            
            elif p[1]<=self.pos[1]+self.height+self.near_range: # below y max
                print("approach y max")
                collide_ymax, x_pred = calc_collision_in_y(p, v, self.pos[1]+self.height, self.pos[0], self.pos[0]+self.width)
                
                if collide_ymax == True:
                    d = math.dist(p, [x_pred, self.pos[1]+self.height])
                    theta = ((1/d) * (90-15)) + 15
                    
                # if grad +, rotate vel clockwise, -theta
                if v[0] < 0: # x going down
                    theta *= -1
                # if grad -, rotate vel anticlockwise, +theta
                # redundant to include this part of the if
                # print(f"theta: {theta}")
                turn = np.array([v[0]*cos(theta) - v[1]*sin(theta), v[0]*sin(theta) + v[1]*cos(theta)])
                
            steer_away += turn # add turn
            
            # steer_away = steer_away / np.linalg.norm(steer_away)
        
        return steer_away