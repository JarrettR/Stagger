import itertools

class Iterator(object):
    def __init__(self, system):
        self.system = system
        self.i = 0
        self.iterables = []
        self.iteratedList = "aaa"

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < len(self.iteratedList):
            params = self.iteratedList[self.i]
            self.i = self.i + 1
            print(params)
            return self
        else:
            raise StopIteration()
            
    #('drive1', 'x', -20, 20, 1))  
    def add_iterator(self, parameters):
        if self.check_component_exists(parameters[0]):
            self.iterables.append(parameters)
        else:
            raise ValueError('Component does not exist in system!')
            
    def bake(self):
        line = []
        listOut = []
        x = 0
        for line in self.iterables:
            print(line)
            print(line[0], line[1])
            for value in range(line[2], line[3], line[4]):
                print(value)
                listOut.append((line[0], line[1], value, ))
            x += 1
        print(listOut)
        print('----')
        print(*listOut)
        print('----')
        #for out in itertools.product(*listOut):
        #    print(out)
        
        
    def check_component_exists(self, component):
        if component in self.system.get_members():
            return True
        else:
            return False
    
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
        