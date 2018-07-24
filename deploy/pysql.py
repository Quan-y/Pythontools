# -*- coding: utf-8 -*-
"""
===============================================================================
===================== PYTHON SQLITE API BASED ON DATAFRAME ====================
===============================================================================
@author: QUAN YUAN
"""
import sqlite3
from pandas.io import sql
import pandas as pd

# Database class
class Database:
    '''
    Database = sql.Database(name = 'orgdata.db', data = )
    '''
    def __init__(self, name):
        # the name of the database name.db
        self.name = name
        # data: dataframe structures
        # self.data = data
        
    # add new table in 'name.db', if 'name.db' is not exit, create 'name.db'
    def df_table(self, data, table, key = None):
        '''
        data: DataFrame type
        table: table name
        key: not working
        '''
        # if exist, don't do anything
        # chunk import data, 1000 rows data/one time
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        sql.to_sql(data, name = table, con = conn, \
                   if_exists = 'fail', chunksize = 1000, index = False)
        # not working right now, you have to use newtable to create a new table with keys at first
        # key: default value: index of dataframe
        if key == None:
            # ERROR AND NOT FIXED......
            try:
                c.execute("Alter table " + table + " Add Constraint ppp Primary Key (index)")
            except:
                pass
        else:
            try:
                c.execute("Alter table " + table + " Add Constraint ppp Primary Key " + key)
            except:
                pass
        
        conn.commit()
        conn.close()
    
    # ADD A NEW TABLE WITH KEYS
    def new_table(self, table, col, col_type, key):
        '''
        table: table name, string
        col: column name, list
        col_type: column type, list
        key: key name, list
        '''
        # construct column and column type string
        col_str = ''
        for each_col, each_col_type in zip(col, col_type):
            col_str += (each_col + ' ' + each_col_type + ', ')
            
        # construct key
        key_str = ''
        for each_key in key:
            key_str += (each_key + ', ')
        col_str += ('PRIMARY KEY (' + key_str[:-2] + ')')
        
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        print "CREATE TABLE " + table + " (" + col_str + ")"
        c.execute("CREATE TABLE " + table + " (" + col_str + ")")
        conn.commit()
        conn.close()
    
    # ADD A NEW COLUMNS
    def new_column(self, table, col, col_type):
        '''
        table: table name, string
        col: column name, string
        col_type: column type, string
        '''
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        c.execute("alter table " + table + " add column " + col + " " + col_type)
        conn.commit()
        conn.close()
    
    # ADD A NEW DATABASE
    def bd(self):
        conn = sqlite3.connect(self.name)
        conn.commit()
        conn.close()
    
    # ADD NEW DATA TO THE TABLE
    # new_data: dataframe, the index of the dataframe must be unique since the key 
    def add(self, data, table):
        conn = sqlite3.connect(self.name)
        sql.to_sql(data, name = table, con = conn, \
                   if_exists = 'append', chunksize = 1000, index = False)
        conn.commit()
        conn.close()
    
    # UPDATE DATA
    def update(self, data, table, key):
        '''
        update monthdiff set Brent_mf_1_2 = 1 where date = '2018-06-14 00:00:00' and fields = 'px_last'
        data: dataframe
        table: table name
        key: key list
        '''
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        # for each line of data
        for i in range(len(data)):
            # for each value and key
            update_str = ''
            condition_str = ''
            # construct update string
            for each_key, each_values in zip(data.iloc[i].drop(key).keys(), \
                                             data.iloc[i].drop(key).values):
                update_str += (each_key + ' = ' + str(each_values) + ', ')
            # drop the last ,
            update_str = update_str[:-2]
            # construct condition string
            for each_key, each_values in zip(data.iloc[i][key].keys(), \
                                             data.iloc[i][key].values):
                condition_str += (each_key + ' = "' + str(each_values) + '" and ')
            # drop the last ,
            condition_str = condition_str[:-5]
#            print "update " + table + " set " + update_str +  " where " + condition_str
            # execute sql
            c.execute("update " + table + " set " + update_str +  " where " + condition_str)
        conn.commit()
        conn.close()
    
    # DELETE DATA FROM DATABASE
    def delete(self, table, key, key_name = 'index'):
        '''
        table: table name
        key: which key
        key_name: key name
        NOTICE: This method still need alter!
        '''
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        c.execute("DELETE from " + table + " where " + self.key_name + " = "+ self.key)
        conn.commit()
        conn.close()
        
    # READ DATA FROM SQLITE
    def read(self, table = None, sql = 'SELECT * FROM '):
        '''
        table: table name
        sql: SQL language
        Can be used to read data or only used to read SQL
        '''
        conn = sqlite3.connect(self.name)
        if sql == 'SELECT * FROM ':
            sql = 'SELECT * FROM '+ table
        else:
            pass
        df = pd.read_sql(sql, conn)
        return df
    
    # READ SQL Language
    def sql(self, sql):
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
    
    # INSERT
    def insert(self, data, table):
        '''
        INSERT INTO oildata(date, Brent_mf_1_2, Brent_mf_1_3) VALUES ('2018-06-04', 1, 2)
        data: dataframe
        table: table name, string
        key: key list ['date']
        '''
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        # key tuple
        key_tuple = tuple([each.encode('utf-8') for each in data.columns])
        # for each line of data
        for i in range(len(data)):
            # value tuple
            value_tuple = tuple(data.iloc[i].values)
#            print 'INSERT INTO ' + table + str(key_tuple) + ' VALUES ' + str(value_tuple)
            # execute sql
            try:
                c.execute('INSERT INTO ' + table + str(key_tuple) + ' VALUES ' + str(value_tuple))
            except:
                pass
        conn.commit()
        conn.close()
        
        
        