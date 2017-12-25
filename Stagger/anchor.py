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
        return self.r * np.cos(np.deg2rad(angle)), self.r * np.sin(np.deg2rad(angle))