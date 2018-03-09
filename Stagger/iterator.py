import itertools

class Iterator(object):
    def __init__(self, system):
        self.system = system
        self.iterables = []
        self.maxIndex = []
        self.currentIndex = []

    def __iter__(self):
        return self

    def __next__(self):
        if self.decrement_pointer() == True:
            parameters = self.calculate_parameters(self.currentIndex)
            self.update_system(parameters)
            return self
        else:
            raise StopIteration()
            
    #parameters = ('drive1', 'x', -20, 20, 1)
    def add_iterator(self, parameters):
        if self.check_component_exists(parameters[0]):
            self.iterables.append(parameters)
        else:
            raise ValueError('Component does not exist in system!')
            
    def bake(self):
        x = 0
        for line in self.iterables:
            steps = int((line[3] - line[2]) / line[4])
            self.maxIndex.append(steps)
        self.currentIndex = list(self.maxIndex)
        
    def check_component_exists(self, component):
        if component in self.system.get_members():
            return True
        else:
            return False
        
    def decrement_pointer(self):
        for x in range(len(self.currentIndex), 0, -1):
            if self.currentIndex[x - 1] > 0:
                self.currentIndex[x - 1] -= 1
                if x < len(self.currentIndex):
                    self.currentIndex[x] = self.maxIndex[x]
                break
            elif x == 1:
                return False
        return True
    
    def calculate_parameters(self, values):
        parameters = []
        for index, item in enumerate(values):
            min = self.iterables[index][2]
            resolution = self.iterables[index][4]
            value = (item * resolution) + min
            
            parameters.append((self.iterables[index][0], self.iterables[index][1], value, ))
            
        return parameters
        
        
    def update_system(self, parameters):
        for member in parameters:
            self.system.set_value(*member)
    
    def create_parameter(self, parameter, min, max, resolution):
    
        #self.parameter = parameter
        #self.min = min
        #self.max = max
        #self.resolution = resolution
        return (parameter, min, max, resolution)
        
    def print_parameter(self, parameter):
    
        print(parameter)
        
    def print_iterables(self):
    
        print(self.iterables)
        