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
        finally:
            self.conn.close()
            
            
    def create_table(self, create_table_sql)
    
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
       
    def create_default_tables(self):
        sql_system = """ CREATE TABLE IF NOT EXISTS systems (
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
                        anchor1_speed integer NOT NULL,
                        anchor1_initial integer NOT NULL,
                        anchor2_x real NOT NULL,
                        anchor2_y real NOT NULL,
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
                        FOREIGN KEY (system_id) REFERENCES systems (id)
                    );"""
 
        if self.conn is not None:
            create_table(sql_system)
            
            create_table(sql_parameters)
            
            create_table(sql_points)
        else:
            print("Error! Cannot create DB connection.")