import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import fractions
import stagger

bar1 = { 'length': 35, 'joint': 30 }
bar2 = { 'length': 40 }

drive1 = stagger.Anchor(-20, -20, 10, 50, 50)
drive2 = stagger.Anchor(15, -22, 6, 20, 180)

fig = plt.figure(figsize=(6, 6))
ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
line1, = ax.plot([], [], 'b-', lw=8)
line2, = ax.plot([], [], 'g-', lw=8)
endLine, = ax.plot([], [], 'b:', lw=5)

patches = []
circle = Circle((drive1.x, drive1.y), drive1.r, fc='m')
patches.append(circle)
circle = Circle((drive2.x, drive2.y), drive2.r, fc='r')
patches.append(circle)


patchBar1Base = plt.Circle((5, -5), 1.5, fc='y')
patchBar2Base = plt.Circle((5, -5), 1.5, fc='y')
patchBar2End = plt.Circle((5, -5), 1.5, fc='y')

patchJoint = plt.Circle((5, -5), 1.5, fc='y')
patchJointArc = plt.Circle((5, -5), bar1['joint'], fc='y', alpha=0.2, fill=False)
patchBar2Arc = plt.Circle((5, -5), bar2['length'], fc='y', alpha=0.2, fill=False)

p = PatchCollection(patches)
ax.add_collection(p)


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
    Drive1X, Drive1Y = drive1.base_point(i)

    patchBar1Base.center = (Drive1X, Drive1Y)
    patchJointArc.center = (Drive1X, Drive1Y)
    
    #drive 2
    x1, y1 = drive2.base_point(i)

    patchBar2Base.center = (x1, y1)
    patchBar2Arc.center = (x1, y1)
    driveLengthR, driveAngle = drive1.distance_from(x1, y1)
    
    angle = stagger.Two_Bar.cosine_law(bar1['joint'], driveLengthR, bar2['length'])
    x2, y2 = stagger.Two_Bar.line_end(Drive1X, Drive1Y, bar1['length'], angle + driveAngle)
    
    line1.set_data([Drive1X, x2], [Drive1Y, y2])
    patchJoint.center = stagger.Two_Bar.line_end(Drive1X, Drive1Y, bar1['joint'], angle + driveAngle)
    patchBar2End.center = (x2, y2)
    
    angle = stagger.Two_Bar.cosine_law( bar2['length'], driveLengthR,bar1['joint'])
    x2, y2 = stagger.Two_Bar.line_end(x1, y1, bar2['length'], (np.pi - angle) + driveAngle)
    line2.set_data([x1, x2], [y1, y2])
    
    return line1, line2, patchBar1Base, patchBar2Base, patchJoint, patchJointArc, patchBar2Arc, patchBar2End,
    
anim = animation.FuncAnimation(fig, animateFrame, init_func=init,
                               frames=360, interval=50, blit=True)
                               


last = stagger.Two_Bar.end_path(stagger.Two_Bar, drive1, drive2, bar1, bar2, 0)
for i in range(360):
    next = stagger.Two_Bar.end_path(stagger.Two_Bar, drive1, drive2, bar1, bar2, i)
    if i > 0:
        plt.plot([last[0], next[0]], [last[1], next[1]], 'k-')
    last = next

plt.show()