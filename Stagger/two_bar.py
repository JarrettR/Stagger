import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import fractions
from . import Anchor
from . import Bar

class Two_Bar(object):
    def __init__(self, drive1, drive2, bar1, bar2):
    
        self.drive1 = drive1
        self.drive2 = drive2
        self.bar1 = bar1
        self.bar2 = bar2
    
        if (drive1.distance_angle_from(drive2.x, drive2.y)[0] + drive1.r + drive2.r) >= (bar1.joint + bar2.length):
            raise NameError('Bars too short!')
        if ((drive1.distance_angle_from(drive2.x, drive2.y)[0] - drive1.r) + bar1.joint) < (bar2.length):
            raise NameError('Bars too long!')
        
        #identify speeds
        self.animationSpeed = self.lcm(drive1.speed, drive2.speed)
        
        
    def lcm(self, a,b): return abs(a * b) / fractions.gcd(a,b) if a and b else 0

    def sides_to_angle(self, A, B, C):
        #cosine law
        out = np.arccos((A * A + B * B - C * C)/(2.0 * A * B))
        return out
        
    def line_end(self, x, y, r, angle):
        x = x + np.cos(angle) * r
        y = y + np.sin(angle) * r
        return x, y
        
    def end_path(self, i):
        #drive 1
        drive1X, drive1Y = self.drive1.base_point(i)
        
        #drive 2
        drive2X, drive2Y = self.drive2.base_point(i)
        
        driveLengthR, driveAngle = self.drive1.base_point_distance(i, self.drive2)
        
        angle = self.sides_to_angle(self.bar1.joint, driveLengthR, self.bar2.length)
        
        barEnd = self.line_end(drive1X, drive1Y, self.bar1.length, angle + driveAngle)
        
        return barEnd

    def define_speed(self):
        if drive1.speed == 0:
            animate['frames'] = 360 / np.abs(drive2.speed)
            animate['delay'] = 100 / np.abs(drive2.speed)
        elif drive2.speed == 0:
            animate['frames'] = 360 / np.abs(drive1.speed)
            animate['delay'] = 100 / np.abs(drive1.speed)
        elif np.abs(drive1.speed) > np.abs(drive2.speed):
            lcm = lcm(np.abs(drive1.speed), np.abs(drive2.speed))
            print(lcm)
            animate['frames'] = int(lcm)
            lowest = lcm / np.abs(drive2.speed)
            animate['frames'] = int(lowest) * 360
            
            drive2['interval'] = 360 * lowest * drive2.speed
            print(drive2['interval'])
            #drive2['interval'] = (lcm / drive1.speed) / 360
            
            drive1['interval'] = drive1.speed
            
            animate['delay'] = 100 # / np.abs(drive2.speed)
            #animate = { 'delay': 100 / np.abs(drive2.speed), 'frames':  np.abs(drive2.speed)}
            speed2 = 1
            speed1 = np.abs(drive1.speed / drive2.speed)
        else:
            lcm = lcm(np.abs(drive1.speed), np.abs(drive2.speed))
            print(lcm)
            animate = { 'delay': 100 / np.abs(drive1.speed), 'frames':  np.abs(drive1.speed)}
            speed1 = 1
            speed2 = np.abs(drive2.speed / drive1.speed)
    