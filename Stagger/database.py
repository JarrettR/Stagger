import sqlite3
from sqlite3 import Error
 
 
class Database(object):
    def __init__(self, filename):
        self.create_connection(filename)
    
    def create_connection(self, filename):
    
        try:
            self.conn = sqlite3.connect(filename)
            
        except Error as e:
            print(e)
            
            
    def close_connection(self):
        self.conn.close()
        
        
    def create_table(self, sql):
    
        try:
            c = self.conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)
       
    def create_default_tables(self):
        sql_system = """ CREATE TABLE IF NOT EXISTS studies (
                        id integer PRIMARY KEY,
                        name text NOT NULL
                    ); """
                    
        sql_parameters = """ CREATE TABLE IF NOT EXISTS parameters_2bar (
                        id integer PRIMARY KEY,
                        system_id integer NOT NULL,
                        name text,
                        bar1_length real NOT NULL,
                        bar1_joint real NOT NULL,
                        bar2_length real NOT NULL,
                        anchor1_x real NOT NULL,
                        anchor1_y real NOT NULL,
                        anchor1_r real NOT NULL,
                        anchor1_speed integer NOT NULL,
                        anchor1_initial integer NOT NULL,
                        anchor2_x real NOT NULL,
                        anchor2_y real NOT NULL,
                        anchor2_r real NOT NULL,
                        anchor2_speed integer NOT NULL,
                        anchor2_initial integer NOT NULL
                    ); """
     
        sql_points = """CREATE TABLE IF NOT EXISTS points (
                        id integer PRIMARY KEY,
                        system_id integer NOT NULL,
                        x real NOT NULL,
                        y real NOT NULL,
                        vector_distance real NOT NULL,
                        vector_angle real NOT NULL,
                        FOREIGN KEY (system_id) REFERENCES studies (id)
                    );"""
 
        if self.conn is not None:
            self.create_table(sql_system)
            
            self.create_table(sql_parameters)
            
            self.create_table(sql_points)
        else:
            print("Error! Cannot create DB connection.")
            
    def insert_study(self, name):
        sql = ''' INSERT INTO studies(name)
                  VALUES(?) '''
        try:
            c = self.conn.cursor()
            c.execute(sql, (name,))
            self.conn.commit()
        except Error as e:
            print(e)
            
        return c.lastrowid
        
    def insert_parameters(self, id, name, study):
        #Todo: Check motion system type (eg. 2 bar, 4 bar)
        sql = ''' INSERT INTO parameters_2bar(
                system_id, name, bar1_length, bar1_joint, bar2_length, anchor1_x, anchor1_y, anchor1_r, anchor1_speed, anchor1_initial, anchor2_x, anchor2_y, anchor2_r, anchor2_speed, anchor2_initial)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
                  
        try:
            c = self.conn.cursor()
            c.execute(sql, (id, name) + study.parameters)
            self.conn.commit()
        except Error as e:
            print(e)
            
    def insert_endpoints(self, id, data):
        sql = ''' INSERT INTO points(system_id, x, y, vector_distance, vector_angle)
                  VALUES(?,?,?,?,?) '''
                  
        #print(data)
        #print((id, ) + data)
        try:
            c = self.conn.cursor()
            #map((lambda x: print(sql,(id, ) + x)), data)
            #map(print, data)
            first = True
            vector_distance = 0
            vector_angle = 0
            
            for x in data:
                if not first:
                    vector_distance = 0
                    vector_angle = 0
                    #From Anchor
                    #theta = self.xy_to_angle((self.x - x), (self.y - y))
                    #distance = self.xy_to_hyp((x - self.x), (y - self.y))
                    
                first = False
                    
                c.execute(sql,(id, ) + x + (vector_distance, vector_angle))
                
            self.conn.commit()
            
        except Error as e:
            print(e)
    