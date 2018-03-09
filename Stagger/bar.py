
class Bar(object):

    def __init__(self, length, joint = 0):
        self.length = length
        self.joint = joint
             
    def set_value(self, parameter, value):
        if parameter == 'length':
            self.length = value
        elif parameter == 'joint':
            self.joint = value
        else:
            raise ValueError('Parameter does not exist!')