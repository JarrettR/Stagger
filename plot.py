import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection

drive1 = { 'x': -20, 'y': -20, 'r': 10, 'speed': 50 , 'initial': 0 }
drive2 = { 'x': 15, 'y': -22, 'r': 8, 'speed': 10 , 'initial': 180 }
bar1 = { 'length': 45, 'joint': 30 }
bar2 = { 'length': 25 }

fig = plt.figure(figsize=(6, 6))
ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
line1, = ax.plot([], [], 'b-', lw=8)
line2, = ax.plot([], [], 'g-', lw=8)

#speed
if drive1['speed'] > drive2['speed']:
    speed2 = 1
    speed1 = drive1['speed'] / drive2['speed']
    interval = 100 / drive2['speed']
else:
    speed1 = 1
    speed2 = drive2['speed'] / drive1['speed']
    interval = 100 / drive1['speed']

patches = []
circle = Circle((drive1['x'], drive1['y']), drive1['r'])
patches.append(circle)
circle = Circle((drive2['x'], drive2['y']), drive2['r'])
patches.append(circle)


patchBar1Base = plt.Circle((5, -5), 1.5, fc='y')
patchBar2Base = plt.Circle((5, -5), 1.5, fc='y')

patchJoint = plt.Circle((5, -5), 1.5, fc='y')
patchJointArc = plt.Circle((5, -5), bar1['joint'], fc='y', alpha=0.2, fill=False)
patchBar2Arc = plt.Circle((5, -5), bar2['length'], fc='y', alpha=0.2, fill=False)

colors = 100*np.random.rand(len(patches))
p = PatchCollection(patches)
p.set_array(np.array(colors))
ax.add_collection(p)

def cosine_law(A, B, C):
    print(A, B, C)
    out = np.arccos((A * A + B * B - C * C)/(2.0 * A * B))
    return out
    
def line_end(X, Y, R, T):
    x = X + np.cos(T) * R
    y = Y + np.sin(T) * R
    print (x, y)
    return x, y


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
    
    return line1, line2, patchBar1Base, patchBar2Base, patchJoint, patchJointArc, patchBar2Arc,

    
def animate(i):

    #drive 1
    Drive1X, Drive1Y = drive1['r'] * np.cos(np.deg2rad(i)), drive1['r'] * np.sin(np.deg2rad(i))
    
    Drive1X = Drive1X + drive1['x']
    Drive1Y = Drive1Y + drive1['y']
    
    patchBar1Base.center = (Drive1X, Drive1Y)
    patchJointArc.center = (Drive1X, Drive1Y)
    
    #drive 2
    x1, y1 = drive2['r'] * np.cos(np.deg2rad(180 - i)), drive2['r'] * np.sin(np.deg2rad(180 - i))
    
    x1 = x1 + drive2['x']
    y1 = y1 + drive2['y']
    
    patchBar2Base.center = (x1, y1)
    patchBar2Arc.center = (x1, y1)
    
    driveAngle = np.arctan((Drive1Y - y1) / (Drive1X - x1))
    
    driveLengthR = np.sqrt((x1 - Drive1X)**2 + (y1 - Drive1Y)**2)
    angle = cosine_law(bar1['joint'], driveLengthR, bar2['length'])
    x2, y2 = line_end(Drive1X, Drive1Y, bar1['length'], angle + driveAngle)
    print(driveLengthR, angle, x2, y2)
    line1.set_data([Drive1X, x2], [Drive1Y, y2])
    patchJoint.center = line_end(Drive1X, Drive1Y, bar1['joint'], angle + driveAngle)
    
    angle = cosine_law( bar2['length'], driveLengthR,bar1['joint'])
    x2, y2 = line_end(x1, y1, bar2['length'], (np.pi - angle) + driveAngle)
    line2.set_data([x1, x2], [y1, y2])
    
    #patchJoint.center = (x2, y2)
    
    print(i)
    return line1, line2, patchBar1Base, patchBar2Base, patchJoint, patchJointArc, patchBar2Arc,

    
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=360, interval=interval, blit=True)


plt.show()