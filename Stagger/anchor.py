import numpy as np

class Anchor(object):

    def __init__(self, x, y, r, speed=1, initial=0):

        self.x = x
        self.y = y
        self.r = r
        self.speed = speed
        self.initial = initial

    @property
    def xy(self):
        return (self.x, self.y)


    def base_point(self, angle):
        """returns base point of current object

        The base point in this context is the point at which
        the linkage attaches to the rotating driveshaft,
        at the given angle.
        """
        if self.speed < 0:
            angle = self.initial - angle
        else:
            angle = self.initial + angle
        x = (self.r * self.deg_to_x(angle)) + self.x
        y = (self.r * self.deg_to_y(angle)) + self.y

        return x, y

    def set_value(self, parameter, value):
        if parameter == 'x':
            self.x = value
        elif parameter == 'y':
            self.x = value
        elif parameter == 'r':
            self.x = value
        elif parameter == 'speed':
            self.x = value
        else:
            raise ValueError('Parameter does not exist!')

    def distance_angle_from(self, x, y):
        """returns distance and angle from current object

        Given an arbitrary set of coordinates,
        will return distance from the current object
        """
        theta = self.xy_to_angle((self.x - x), (self.y - y))
        distance = self.xy_to_hyp((x - self.x), (y - self.y))

        return distance, theta

    def base_point_distance(self, angle1, angle2, end):
        """returns distance between two base points

        Given the current object and a second object,
        calculates the x/y distance between them, at
        their respective angles.
        """
        startPoint = self.base_point(angle1)
        endPoint = end.base_point(angle2)

        x = startPoint[0] - endPoint[0]
        y = startPoint[1] - endPoint[1]

        theta = self.xy_to_angle(x, y)
        distance = self.xy_to_hyp(x, y)

        return distance, theta

    @staticmethod
    def deg_to_x(angle):
        return np.cos(np.deg2rad(angle))

    @staticmethod
    def deg_to_y(angle):
        return np.sin(np.deg2rad(angle))

    @staticmethod
    def xy_to_angle(x, y):
        return np.arctan(y / x)

    @staticmethod
    def xy_to_hyp(x, y):
        return np.sqrt((x)**2 + (y)**2)
