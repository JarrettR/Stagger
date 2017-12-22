import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import fractions

class 2bar(object):
    def init(self, 

drive1 = { 'x': -20, 'y': -20, 'r': 10, 'speed': 50, 'initial': 0 }
drive2 = { 'x': 15, 'y': -22, 'r': 8, 'speed': 20, 'initial': 180 }
bar1 = { 'length': 35, 'joint': 30 }
bar2 = { 'length': 40 }

fig = plt.figure(figsize=(6, 6))
ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
line1, = ax.plot([], [], 'b-', lw=8)
line2, = ax.plot([], [], 'g-', lw=8)
endLine, = ax.plot([], [], 'b:', lw=5)

def lcm(a,b): return abs(a * b) / fractions.gcd(a,b) if a and b else 0

#speed
animate = { }
if drive1['speed'] == 0:
    animate['frames'] = 360 / np.abs(drive2['speed'])
    animate['delay'] = 100 / np.abs(drive2['speed'])
elif drive2['speed'] == 0:
    animate['frames'] = 360 / np.abs(drive1['speed'])
    animate['delay'] = 100 / np.abs(drive1['speed'])
elif np.abs(drive1['speed']) > np.abs(drive2['speed']):
    lcm = lcm(np.abs(drive1['speed']), np.abs(drive2['speed']))
    print(lcm)
    animate['frames'] = int(lcm)
    lowest = lcm / np.abs(drive2['speed'])
    animate['frames'] = int(lowest) * 360
    
    drive2['interval'] = 360 * lowest * drive2['speed']
    print(drive2['interval'])
    #drive2['interval'] = (lcm / drive1['speed']) / 360
    
    drive1['interval'] = drive1['speed']
    
    animate['delay'] = 100 # / np.abs(drive2['speed'])
    #animate = { 'delay': 100 / np.abs(drive2['speed']), 'frames':  np.abs(drive2['speed'])}
    speed2 = 1
    speed1 = np.abs(drive1['speed'] / drive2['speed'])
else:
    lcm = lcm(np.abs(drive1['speed']), np.abs(drive2['speed']))
    print(lcm)
    animate = { 'delay': 100 / np.abs(drive1['speed']), 'frames':  np.abs(drive1['speed'])}
    speed1 = 1
    speed2 = np.abs(drive2['speed'] / drive1['speed'])



    
patches = []
circle = Circle((drive1['x'], drive1['y']), drive1['r'], fc='m')
patches.append(circle)
circle = Circle((drive2['x'], drive2['y']), drive2['r'], fc='r')
patches.append(circle)


patchBar1Base = plt.Circle((5, -5), 1.5, fc='y')
patchBar2Base = plt.Circle((5, -5), 1.5, fc='y')
patchBar2End = plt.Circle((5, -5), 1.5, fc='y')

patchJoint = plt.Circle((5, -5), 1.5, fc='y')
patchJointArc = plt.Circle((5, -5), bar1['joint'], fc='y', alpha=0.2, fill=False)
patchBar2Arc = plt.Circle((5, -5), bar2['length'], fc='y', alpha=0.2, fill=False)

p = PatchCollection(patches)
ax.add_collection(p)

def cosine_law(A, B, C):
    out = np.arccos((A * A + B * B - C * C)/(2.0 * A * B))
    return out
    
def line_end(X, Y, R, T):
    x = X + np.cos(T) * R
    y = Y + np.sin(T) * R
    return x, y
    
def base_point(drive, i):
    if drive['speed'] < 0:
        i = drive['initial'] - i
    else:
        i = drive['initial'] + i
    return drive['r'] * np.cos(np.deg2rad(i)), drive['r'] * np.sin(np.deg2rad(i))
    
def distance_between(obj1, obj2):
    theta = np.arctan((obj1['y'] - obj2['y']) / (obj1['x'] - obj2['x']))
    distance = np.sqrt((obj2['x'] - obj1['x'])**2 + (obj2['y'] - obj1['y'])**2)
    
    return distance, theta
    
def end_path(drive1, drive2, bar1, bar2, i):
    #drive 1
    Drive1X, Drive1Y = base_point(drive1, i)
    
    Drive1X = Drive1X + drive1['x']
    Drive1Y = Drive1Y + drive1['y']

    #drive 2
    Drive2X, Drive2Y = base_point(drive2, i)
    
    Drive2X = Drive2X + drive2['x']
    Drive2Y = Drive2Y + drive2['y']

    driveAngle = np.arctan((Drive1Y - Drive2Y) / (Drive1X - Drive2X))
    
    driveLengthR = np.sqrt((Drive2X - Drive1X)**2 + (Drive2Y - Drive1Y)**2)
    angle = cosine_law(bar1['joint'], driveLengthR, bar2['length'])
    
    return line_end(Drive1X, Drive1Y, bar1['length'], angle + driveAngle)


def init():
    line1.set_data([], [])
    line2.set_data([], [])
    patchBar1Base.center = (5, 5)
    patchBar2Base.center = (5, 5)
    patchJoint.center = (5, 5)
    
    ax.add_patch(patchBar1Base)
    ax.add_patch(patchBar2Base)
    ax.add_patch(patchJoint)
    ax.add_patch(patchJointArc)
    ax.add_patch(patchBar2Arc)
    ax.add_patch(patchBar2End)
    
    return line1, line2, patchBar1Base, patchBar2Base, patchJoint, patchJointArc, patchBar2Arc, patchBar2End,

    
def animateFrame(i):

    #drive 1
    Drive1X, Drive1Y = base_point(drive1, i * drive1['interval'])
    
    Drive1X = Drive1X + drive1['x']
    Drive1Y = Drive1Y + drive1['y']
    
    patchBar1Base.center = (Drive1X, Drive1Y)
    patchJointArc.center = (Drive1X, Drive1Y)
    
    #drive 2
    x1, y1 = base_point(drive2, i * drive2['interval'])
    
    x1 = x1 + drive2['x']
    y1 = y1 + drive2['y']
    
    patchBar2Base.center = (x1, y1)
    patchBar2Arc.center = (x1, y1)
    driveLengthR, driveAngle = distance_between({ 'x':Drive1X, 'y': Drive1Y }, { 'x': x1, 'y':y1 })
    #driveAngle = np.arctan((Drive1Y - y1) / (Drive1X - x1))
    
    #driveLengthR = np.sqrt((x1 - Drive1X)**2 + (y1 - Drive1Y)**2)
    angle = cosine_law(bar1['joint'], driveLengthR, bar2['length'])
    x2, y2 = line_end(Drive1X, Drive1Y, bar1['length'], angle + driveAngle)
    
    line1.set_data([Drive1X, x2], [Drive1Y, y2])
    patchJoint.center = line_end(Drive1X, Drive1Y, bar1['joint'], angle + driveAngle)
    patchBar2End.center = (x2, y2)
    
    angle = cosine_law( bar2['length'], driveLengthR,bar1['joint'])
    x2, y2 = line_end(x1, y1, bar2['length'], (np.pi - angle) + driveAngle)
    line2.set_data([x1, x2], [y1, y2])
    
    return line1, line2, patchBar1Base, patchBar2Base, patchJoint, patchJointArc, patchBar2Arc, patchBar2End,

    
anim = animation.FuncAnimation(fig, animateFrame, init_func=init,
                               frames=animate['frames'], interval=animate['delay'], blit=True)

                               
                               
if (distance_between(drive1, drive2)[0] + drive1['r'] + drive2['r']) >= (bar1['joint'] + bar2['length']):
    raise NameError('Bars too short!')
if ((distance_between(drive1, drive2)[0] - drive1['r']) + bar1['joint']) < (bar2['length']):
    raise NameError('Bars too long!')
    

last = end_path(drive1, drive2, bar1, bar2, 0)
for i in range(360):
    next = end_path(drive1, drive2, bar1, bar2, i)
    if i > 0:
        plt.plot([last[0], next[0]], [last[1], next[1]], 'k-')
    last = next

plt.show()