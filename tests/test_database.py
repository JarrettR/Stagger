# -*- coding: utf-8 -*-

from .context import stagger
import os
import sqlite3
import unittest

class TestDatabase(unittest.TestCase):
    '''
    Database test cases.
    '''
    
    def test_stagger(self):
        '''Todo: End to end'''
        assert True
        
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
        
 
    def setUp(self):
        '''Setup temp database'''
        self.create_database('testdb.db')
        
    def tearDown(self):
        '''Delete database'''
        os.remove('testdb.db')
        
    def test_db_creation(self):
        '''Test that the DB gets created'''

        assert False
        #self.assertEqual(motionSystem.totalFrames, 360)

        
if __name__ == '__main__':
    unittest.main()