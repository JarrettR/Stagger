# -*- coding: utf-8 -*-

from .context import stagger

import unittest

class TestIteration(unittest.TestCase):
    """Iteration test cases."""
    
    def test_iteration(self):
        '''Todo: End to end'''
        assert False
        
    def test_iteration_setup(self):
        '''Check iteratable setup'''
        #self.iteratable

        assert False

    def test_iteration_count_single(self):
        '''Iterable iterates'''
        #self.iteratable

        assert False

    def test_iteration_count_recursion(self):
        '''Iterable recursively iterates (double layer)'''
        #self.iteratable

        assert False

    def test_iteration_count_recursion(self):
        '''Iterable recursively iterates (triple layer)'''
        #self.iteratable

        assert False


    def setUp(self):
        '''Setup iteratable'''
        
        #(length, joint = 0)
        bar1 = stagger.Bar(35, 30)
        bar2 = stagger.Bar(40)

        #(x, y, r, speed = 1, initial = 0)
        drive1 = stagger.Anchor(-20, -20, 10, 3, 0)
        drive2 = stagger.Anchor(15, -22, 6, 6, 180)
        
        self.motionSystem = stagger.TwoBar(drive1, drive2, bar1, bar2)
        
        self.iteratable = stagger.Iterator(self.motionSystem)
        
        
if __name__ == '__main__':
    unittest.main()