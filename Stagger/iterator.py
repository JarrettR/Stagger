
class Iterator(object):
    def __init__(self, object):
        self.object = object

    def __iter__(self):
        return self

    def next(self):
        if True:
            return i
        else:
            raise StopIteration()
            
    def add_iterator(self, method, object, parameter):
        pass
    
    def create_parameter(self, parameter, min, max, resolution):
    
        #self.parameter = parameter
        #self.min = min
        #self.max = max
        #self.resolution = resolution
        return (parameter, min, max, resolution)
        