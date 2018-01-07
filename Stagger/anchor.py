import numpy as np

class Anchor(object):

    def __init__(self, x, y, r, speed = 1, initial = 0):
    
        self.x = x
        self.y = y
        self.r = r
        self.speed = speed
        self.initial = initial
        
    def base_point(self, angle):
        if self.speed < 0:
            angle = self.initial - angle
        else:
            angle = self.initial + angle
        x = self.r * np.cos(np.deg2rad(angle)) + self.x
        y = self.r * np.sin(np.deg2rad(angle)) + self.y
        return x, y
        
    def distance_from(self, x, y):
        theta = np.arctan((self.y - y) / (self.x - x))
        distance = np.sqrt((x - self.x)**2 + (y - self.y)**2)
        
        return distance, theta