import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import fractions
import stagger

class GraphAnimation(object):
    def __init__(self):
        #(length, joint = 0)
        self.bar1 = stagger.Bar(35, 30)
        self.bar2 = stagger.Bar(40)

        #(x, y, r, speed = 1, initial = 0)
        self.drive1 = stagger.Anchor(-20, -20, 10, 50, 50)
        self.drive2 = stagger.Anchor(15, -22, 6, 20, 180)

        #xlim, ylim, line1 style, weight, line2 style, weight
        self.init_graph((-50, 50), (-50, 50), 'b-', 8, 'g-', 8)

        #facecolor1, facecolor2
        self.init_circles('m', 'r')


        self.patchbar1Base = plt.Circle((5, -5), 1.5, fc='y')
        self.patchbar2Base = plt.Circle((5, -5), 1.5, fc='y')
        self.patchbar2End = plt.Circle((5, -5), 1.5, fc='y')

        self.patchJoint = plt.Circle((5, -5), 1.5, fc='y')
        self.patchJointArc = plt.Circle((5, -5), self.bar1.joint, fc='y', alpha=0.2, fill=False)
        self.patchbar2Arc = plt.Circle((5, -5), self.bar2.length, fc='y', alpha=0.2, fill=False)

        
        #Begin animation
        
        anim = animation.FuncAnimation(self.fig, self.animate_frame, init_func=self.init_animation,
                               frames=360, interval=50, blit=True)
                               


        #end_path(self.drive1, self.drive2, self.bar1, self.bar2, i)
        last = stagger.Two_Bar.end_path(stagger.Two_Bar, self.drive1, self.drive2, self.bar1, self.bar2, 0)
        for i in range(360):
            next = stagger.Two_Bar.end_path(stagger.Two_Bar, self.drive1, self.drive2, self.bar1, self.bar2, i)
            if i > 0:
                plt.plot([last[0], next[0]], [last[1], next[1]], 'k-')
            last = next

        plt.show()


    def init_graph(self, xlim, ylim, ls1, lw1, ls2, lw2):
        self.fig = plt.figure(figsize=(6, 6))
        self.ax = plt.axes(xlim=xlim, ylim=ylim)
        self.line1, = self.ax.plot([], [], ls1, lw=lw1)
        self.line2, = self.ax.plot([], [], ls2, lw=lw2)

    def init_circles(self, fc1, fc2):
        patches = []
        circle = Circle((self.drive1.x, self.drive1.y), self.drive1.r, fc=fc1)
        patches.append(circle)
        circle = Circle((self.drive2.x, self.drive2.y), self.drive2.r, fc=fc2)
        patches.append(circle)
        p = PatchCollection(patches)
        self.ax.add_collection(p)
        
        
    def init_animation(self):
        self.line1.set_data([], [])
        self.line2.set_data([], [])
        self.patchbar1Base.center = (5, 5)
        self.patchbar2Base.center = (5, 5)
        self.patchJoint.center = (5, 5)
        
        self.ax.add_patch(self.patchbar1Base)
        self.ax.add_patch(self.patchbar2Base)
        self.ax.add_patch(self.patchJoint)
        self.ax.add_patch(self.patchJointArc)
        self.ax.add_patch(self.patchbar2Arc)
        self.ax.add_patch(self.patchbar2End)
        
        return self.line1, self.line2, self.patchbar1Base, self.patchbar2Base, self.patchJoint, self.patchJointArc, self.patchbar2Arc, self.patchbar2End,

        
    def animate_frame(self, i):

        #drive 1
        self.drive1X, self.drive1Y = self.drive1.base_point(i)

        self.patchbar1Base.center = (self.drive1X, self.drive1Y)
        self.patchJointArc.center = (self.drive1X, self.drive1Y)
        
        #drive 2
        x1, y1 = self.drive2.base_point(i)

        self.patchbar2Base.center = (x1, y1)
        self.patchbar2Arc.center = (x1, y1)
        driveLengthR, driveAngle = self.drive1.distance_from(x1, y1)
        
        angle = stagger.Two_Bar.cosine_law(self.bar1.joint, driveLengthR, self.bar2.length)
        x2, y2 = stagger.Two_Bar.line_end(self.drive1X, self.drive1Y, self.bar1.length, angle + driveAngle)
        
        self.line1.set_data([self.drive1X, x2], [self.drive1Y, y2])
        self.patchJoint.center = stagger.Two_Bar.line_end(self.drive1X, self.drive1Y, self.bar1.joint, angle + driveAngle)
        self.patchbar2End.center = (x2, y2)
        
        angle = stagger.Two_Bar.cosine_law(self.bar2.length, driveLengthR, self.bar1.joint)
        x2, y2 = stagger.Two_Bar.line_end(x1, y1, self.bar2.length, (np.pi - angle) + driveAngle)
        self.line2.set_data([x1, x2], [y1, y2])
        
        return self.line1, self.line2, self.patchbar1Base, self.patchbar2Base, self.patchJoint, self.patchJointArc, self.patchbar2Arc, self.patchbar2End,
        
if __name__ == '__main__':
    main = GraphAnimation()