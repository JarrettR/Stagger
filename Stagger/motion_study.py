import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import math
from . import Anchor
from . import Bar

class Motion_Study(object):
    def __init__(self, drive1, drive2, bar1, bar2):
        self.resolution = 360
    
        self.drive1 = drive1
        self.drive2 = drive2
        self.bar1 = bar1
        self.bar2 = bar2
        
        self.set_speeds()

    def set_speeds(self):
    
        if self.drive1.speed == self.drive2.speed:
            #Equal (3, 3)
            self.totalFrames = self.resolution
        else:
            gcd = math.gcd(self.drive1.speed, self.drive2.speed)
            
            if gcd > 1:
                if gcd == self.drive1.speed:
                    #Equally divisible (3, 6)
                    self.totalFrames = int((self.drive2.speed / gcd)  * self.resolution)
                elif gcd == self.drive2.speed:
                    #Equally divisible (6, 3)
                    self.totalFrames = int((self.drive1.speed / gcd)  * self.resolution)
                else: 
                    #Common divisor (14, 21)
                    self.totalFrames = int(gcd  * self.resolution)
            else:
                #Coprimes (14, 15)
                self.totalFrames = int(self.drive1.speed * self.drive2.speed  * self.resolution)
                
        self.stepSize = self.totalFrames / self.resolution

    def sides_to_angle(self, A, B, C):
        #cosine law
        out = np.arccos((A * A + B * B - C * C)/(2.0 * A * B))
        return out
        
    def line_end(self, x, y, r, angle):
        x = x + np.cos(angle) * r
        y = y + np.sin(angle) * r
        return x, y
        