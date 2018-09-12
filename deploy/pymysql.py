# -*- coding: utf-8 -*-
"""
Python MySQL 8.0 X Dataframe API
author: @Quan Yuan

Functions:
    (1) create database and table
    (2) insert data from pandas
    (3) update data from pandas (replace or not)
    (4) delete data from table based on index list
    (5) extract data from database and convert it to dataframe object
    (6) execute any SQL
"""
# improt package
import MySQLdb
import sqlalchemy
import pandas as pd

class SQL(object):
    def __init__(self, **para):
        self.para = para
        '''para input: dict with keys of host user password dbase'''
        try:
            self.host = self.para['host']
            self.user = self.para['user'] 
            self.password = self.para['password']
            self.dbase = self.para['dbase']
        except:
            print('Your Input is Wrong, please input a dict with key words \
                   host, user, password, dbase')
        self.db = MySQLdb.connect(self.host, self.user, self.password, self.dbase)
        self.cursor = self.db.cursor()
        self.engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(self.user, self.password, 
                                                      self.host, self.dbase))
    def close(self):
        self.db.close
        return 'CLOSE THE DATABASE'
    
    def newTable(self, table, columns, columns_note, key):
        '''
        table: str
        columns: iter
        columns_note: iter
        key: str
        Example SQL:
            CREATE TABLE `test`.`test_table3`(
                         `id` INT NOT NULL,
                         `sport` VARCHAR(45) NULL,
                          PRIMARY KEY (`id`));
        '''
        str1 = ', '.join([' '.join(each) for each in \
                          list(zip(columns, columns_note))])
        sqlstr = 'CREATE TABLE {0} ({1}, PRIMARY KEY ({2}))'.format(table, \
                               str1, key)
        self.cursor.execute(sqlstr)
        return 'CREATE TABLE {0} WITH COLUMNS {1}'.format(table, columns)
        
    def read(self, table, columns, conditions = None):
        '''read data from database and change to dataframe structure
        table: str
        columns: list
        conditions: str
        '''
        if conditions == None and columns != '*':
            sqlstr = "SELECT {0} FROM {1}".format(', '.join(columns), table)
        elif conditions != None and columns != '*':
            sqlstr = "SELECT {0} FROM {1} WHERE {2}".format(', '.join(columns), \
                          table, conditions)
        elif conditions != None and columns == '*':
            sqlstr = "SELECT * FROM {0} WHERE {1}".format(table, conditions)
        else:
            sqlstr = "SELECT * FROM {0}".format(table)
        # check SQL Language
        # print(sqlstr)
        self.cursor.execute(sqlstr)
        results = self.cursor.fetchall()
        df = pd.DataFrame(list(results), columns = columns)
        return df
    
    def insert(self, table, col_list, value_list):
        '''
        table: str
        col_list: columns names list like [col1, col2, col3]
        value_list: values [[col1 values], [col2 values], [col3 values]]
        example SQL:
            INSERT INTO `test`.`test_table3` (`id`, `sport`) VALUES ('1', 'basketball');
        '''
        
        pass
    
    def dfImport(self, table, df):
        try:
            df.to_sql(con = self.engine, name = table, if_exists = 'append', \
                      chunksize = 1000, index = False)
            print('Success!')
        except:
            print('Import Error')


Testsql = SQL(host = 'localhost', user = 'root', password = 'Yq707197', \
              dbase = 'test')
result = Testsql.read(table = 'test_table', columns = ['name', 'age'], \
                      conditions = "name = 'SY' OR name = 'Hand'")
#Testsql.newTable(table = 'test_table4', columns = ['id', 'single'], \
#                 columns_note = ['int not null', 'boolean null'], key = 'id')
test_df = pd.DataFrame({'id': [1, 2, 3, 4, 5], \
                        'single': [True, False, True, True, True]})
Testsql.dfImport('test_table4', test_df)

#host = 'localhost'
#user = 'root'
#password = 'Yq707197'
#dbase = 'test'
#
#db = MySQLdb.connect(host, user, password, dbase)
#cursor = db.cursor()
#cursor.execute("SELECT * FROM test_table")
#results = cursor.fetchall()
#db.close
