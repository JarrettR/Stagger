import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import math
from . import Anchor
from . import Bar
from . import MotionStudy

class TwoBar(MotionStudy):
    def __init__(self, drive1, drive2, bar1, bar2):
        self.validate_physics(drive1, drive2, bar1, bar2)
        
        super().__init__(drive1, drive2, bar1, bar2)
    
   
    def get_members(self):
        return ['drive1', 'drive2', 'bar1', 'bar2']
        
    def set_value(self, member, parameter, value):
        if member == 'drive1':
            self.drive1.set_value(parameter, value)
        elif member == 'drive2':
            self.drive2.set_value(parameter, value)
        elif member == 'bar1':
            self.bar1.set_value(parameter, value)
        elif member == 'bar2':
            self.bar2.set_value(parameter, value)
        else:
            raise ValueError('Member does not exist!')
        
    def validate_physics(self, drive1, drive2, bar1, bar2):  
        if (drive1.distance_angle_from(drive2.x, drive2.y)[0] + drive1.r + drive2.r) >= (bar1.joint + bar2.length):
            raise ValueError('Bars too short!')
        if ((drive1.distance_angle_from(drive2.x, drive2.y)[0] - drive1.r) + bar1.joint) < (bar2.length):
            raise ValueError('Bars too long!')

            
    def end_path(self, i):        
        #drive 1
        angle1 = i * self.drive1.speed
        drive1X, drive1Y = self.drive1.base_point(angle1)
        
        #drive 2
        angle2 = i * self.drive2.speed
        drive2X, drive2Y = self.drive2.base_point(angle2)
        
        driveLengthR, driveAngle = self.drive1.base_point_distance(angle1, angle2, self.drive2)
        
        angle = self.sides_to_angle(self.bar1.joint, driveLengthR, self.bar2.length)
        
        barEnd = self.line_end(drive1X, drive1Y, self.bar1.length, angle + driveAngle)
        
        return barEnd

    @property
    def parameters(self):
  
        return (self.bar1.length, self.bar1.joint, self.bar2.length, self.drive1.x, self.drive1.y, self.drive1.r, self.drive1.speed, self.drive1.initial, self.drive2.x, self.drive2.y, self.drive2.r, self.drive2.speed, self.drive2.initial)