# -*- coding: utf-8 -*-

import stagger
import pickle
from PIL import Image, ImageDraw, ImageOps
from functools import partial

class GeneratePaths(object):
    def __init__(self):
        #self.save_binary('outputs/test.pickle', system)
        #data = self.load_binary('outputs/test.pickle')
        self.create_database('outputs/test.db')
        
        for y in range(40):
            try:
                system = self.create_system(y - 20)
                self.save_database(self.motionSystem, system)
                #data = self.load_database('outputs/test.db')
                self.save_png('outputs/test{}.png'.format(y), system, 50)
            except (ValueError, ZeroDivisionError) as e:
                print('Could not calculate {}: {}'.format(y, e))
    
    
    def create_system(self, y):
        #(length, joint = 0)
        self.bar1 = stagger.Bar(35, 30)
        self.bar2 = stagger.Bar(40)

        #(x, y, r, speed = 1, initial = 0)
        self.drive1 = stagger.Anchor(y, -20, 10, 6, 0)
        self.drive2 = stagger.Anchor(15, -22, 6, 3, 180)
        
        self.motionSystem = stagger.TwoBar(self.drive1, self.drive2, self.bar1, self.bar2)

        inputRange = list(map((lambda x: x * self.motionSystem.stepSize), range(0,360)))
        
        return list(map(self.motionSystem.end_path, inputRange))

    def save_binary(self, filename, data):
        with open(filename, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


    def load_binary(self, filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        return data

    def create_database(self, filename):
        self.db = stagger.Database(filename)
        self.db.create_default_tables()
        
    def save_database(self, study, data):
        id = self.db.insert_study('Motion Study Name')
        self.db.insert_parameters(id, 'Parameter Set Name', study)
        self.db.insert_endpoints(id, data)


    def load_database(self, filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        return data

    def save_png(self, filename, data, scaling):
        data, boundingBox = self.reposition(data, scaling)
        
        im = Image.new('L', boundingBox, 255)

        draw = ImageDraw.Draw(im)
        
        for i in range(len(data) - 1):
            draw.line(data[i] + data[i + 1], fill=128, width=5)
        del draw
        
        #Image origin is top left, convert to CAD-style bottom left
        im = ImageOps.flip(im)

        im.save(filename, "PNG")

    def flip_y_axis(self, data, height):
        return (data[0], height - data[1])

    def reposition(self, data, scaling = 1):
        '''Returns data, boundingBox'''
        xMin = data[0][0]
        yMin = data[0][1]
        xMax = data[0][0]
        yMax = data[0][1]

        for i in range(len(data)):
            if data[i][0] < xMin:
                xMin = data[i][0]
            if data[i][1] < yMin:
                yMin = data[i][1]
            if data[i][0] > xMax:
                xMax = data[i][0]
            if data[i][1] > yMax:
                yMax = data[i][1]
                
        repoData = []
        
        for i in range(len(data)):
            repoData.append(
                (int((data[i][0] - xMin) * scaling),
                (int((data[i][1] - yMin) * scaling) )))
            
        return repoData, (int((xMax - xMin) * scaling), int((yMax - yMin) * scaling))

        
if __name__ == '__main__':
    main = GeneratePaths()