# -*- coding: utf-8 -*-

from .context import stagger

import unittest
import math


class StaggerTestSuite(unittest.TestCase):
    """Stagger test cases."""
    
    def test_stagger(self):
        '''Todo: End to end'''
        assert True
        
        
    def test_minimum_frames_1(self):
        '''Both speeds are 1'''
        speed1 = 1
        speed2 = 1
        
        motionSystem = self.create_speed_system(speed1, speed2)

        self.assertEqual(motionSystem.totalFrames, 360)
        self.test_step_size(speed1, speed2)
        
    def test_minimum_frames_equal(self):
        '''Both speeds are equal, but not 1'''
        speed1 = 2
        speed2 = 2
        
        motionSystem = self.create_speed_system(speed1, speed2)

        self.assertEqual(motionSystem.totalFrames, 360)
        self.test_step_size(speed1, speed2)
        
    def test_minimum_frames_divisible_1(self):
        '''Speeds are divisible by each other, speed1 lower'''
        speed1 = 3
        speed2 = 6
        
        motionSystem = self.create_speed_system(speed1, speed2)

        self.assertEqual(motionSystem.totalFrames, 720)
        self.test_step_size(speed1, speed2)
        
    def test_minimum_frames_divisible_2(self):
        '''Speeds are divisible by each other, speed2 lower'''
        speed1 = 6
        speed2 = 3
        
        motionSystem = self.create_speed_system(speed1, speed2)

        self.assertEqual(motionSystem.totalFrames, 720)
        self.test_step_size(speed1, speed2)
        
    def test_minimum_frames_coprimes(self):
        '''Speeds are not divisible, lowest common factor is high'''
        speed1 = 14
        speed2 = 15
        
        motionSystem = self.create_speed_system(speed1, speed2)

        self.assertEqual(motionSystem.totalFrames, 75600)
        self.test_step_size(speed1, speed2)
        
        
    def test_minimum_frames_common_divisor(self):
        '''Both speeds are divisible by a different integer'''
        speed1 = 14
        speed2 = 21
        #Divisible by 7
        
        motionSystem = self.create_speed_system(speed1, speed2)

        self.assertEqual(motionSystem.totalFrames, 2520)
        self.test_step_size(speed1, speed2)
        
    def test_step_size(self, speed1 = 1, speed2 = 1):
        '''Step size, resolution, and total frames are related'''
        
        motionSystem = self.create_speed_system(speed1, speed2)

        self.assertEqual(motionSystem.totalFrames, motionSystem.stepSize * motionSystem.resolution)
        
    def create_speed_system(self, speed1, speed2):
        #(length, joint = 0)
        bar1 = stagger.Bar(35, 30)
        bar2 = stagger.Bar(40)

        #(x, y, r, speed = 1, initial = 0)
        drive1 = stagger.Anchor(-20, -20, 10, speed1, 0)
        drive2 = stagger.Anchor(15, -22, 6, speed2, 180)
        
        motionSystem = stagger.Two_Bar(drive1, drive2, bar1, bar2)
        
        #self.motionSystem.totalFrames = 5
        #self.motionSystem.stepSize = 1

        return motionSystem
        

        
if __name__ == '__main__':
    unittest.main()