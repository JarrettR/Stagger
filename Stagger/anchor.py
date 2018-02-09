import numpy as np

class Anchor(object):

    def __init__(self, x, y, r, speed = 1, initial = 0):
    
        self.x = x
        self.y = y
        self.r = r
        self.speed = speed
        self.initial = initial
        
    @property
    def xy(self):
        return (self.x, self.y)
        
        
    def base_point(self, angle):
        if self.speed < 0:
            angle = self.initial - angle
        else:
            angle = self.initial + angle
        x = (self.r * self.deg_to_x(angle)) + self.x
        y = (self.r * self.deg_to_y(angle)) + self.y
        
        return x, y
        
    def distance_angle_from(self, x, y):
        theta = self.xy_to_angle((self.x - x), (self.y - y))
        distance = self.xy_to_hyp((x - self.x), (y - self.y))
        
        return distance, theta
        
    def base_point_distance(self, angle1, angle2, end):
        startPoint = self.base_point(angle1)
        endPoint = end.base_point(angle2)
        
        x = startPoint[0] - endPoint[0]
        y = startPoint[1] - endPoint[1]
        
        theta = self.xy_to_angle(x, y)
        distance = self.xy_to_hyp(x, y)
        
        return distance, theta
        
        
    def deg_to_x(self, angle):
        return np.cos(np.deg2rad(angle))
        
    def deg_to_y(self, angle):
        return np.sin(np.deg2rad(angle))
        
    def xy_to_angle(self, x, y):
        return np.arctan(y / x)
        
    def xy_to_hyp(self, x, y):
        return np.sqrt((x)**2 + (y)**2)