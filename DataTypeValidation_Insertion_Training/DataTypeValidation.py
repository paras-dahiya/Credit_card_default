import shutil
import sqlite3
from datetime import datetime
from os import listdir
import os
import csv
from Application_logging.logger import App_logger

class dBOperation:
    '''
            This class be used for handling all the SQL operation
    '''

    def __init__(self):
        self.path = 'Training_Data/'
        self.badFilePath = "Bad_RawData"
        self.logger = App_logger()


    def dataBaseConnection(self,DatabaseName):
        '''
                        Method Name: dataBaseConnection
                        Description: This Method creates the database with the given name and if Database already exists then opens the connection to the DB.
                        Output: Connection to the DB
                        On failure: Raise ConnectionError
        '''

        try:
            conn = sqlite3.connect(self.path+DatabaseName+'.db')

            file = open("Training_Logs/DatabaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Opened %s database successfully" %DatabaseName)
        except ConnectionError:
            file = open("Training_Logs/DatabaseConnectionLog.txt",'a+')
            self.logger.log(file, "Error while connecting to database: %s" %ConnectionError)
            file.close()
            raise ConnectionError
        return conn

    def createTableDb(self,DatabaseName,column_names):
        '''
                        Method Name: createTableDb
                        Description: This method creates a table in the given database which will be used to insert the Good data after the raw data validation>
                        Output:None
                        On Failure: Raise Exception
        '''
        try:
            conn = self.dataBaseConnection(DatabaseName)
            c=conn.cursor()
            c.execute("SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'Raw_Data'")
            if c.fetchone()[0] ==1:
                conn.close()
                file = open("Training_Logs/DatabaseConnectionLog.txt",'a+')
                self.logger.log(file, "Tables created successfully!!")
                file.close()

                file = open("Training_Logs/DatabaseConnectionLog.txt",'a+')
                self.logger.log(file,"Closed %s database successfully"%DatabaseName)
                file.close()
            else:
                for key in column_names.keys():
                    type = column_names[key]

                    #In try block we check if the table exists, if yes then add columns to the table
                    #else in the catch block we will create the table

                    try:
                        # cur = cur.execute("SELECT name FROM {dbName} WHERE type='table' AND name='Good_Raw_Data'".format(dbName=DatabaseName))
                        conn.execute('ALTER TABLE Raw_Data ADD COLUMN "{column_name}" {dataType}' .format(column_name=key,dataType=type))
                    except:
                        conn.execute('CREATE TABLE  Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))

                conn.close()

                file = open("Training_Logs/DatabaseConnectionLog.txt",'a+')
                self.logger.log(file, "Tables created successfully!!")
                file.close()

                file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
                self.logger.log(file, "Closed %s database successfully" % DatabaseName)
                file.close()

        except Exception as e:
            file = open("Training_Logs/DbTableCreateLog.txt", 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()
            conn.close()
            file = open("Training_Logs/DataBaseConnectionLog.txt", 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()
            raise e
    def insertIntoTable(self,Database):
        '''
                        Method Name: insertIntoTableGoodData
                        Description: This method inserts the Good data files from the Good_Raw folder into the above created table.
                        Output: None
                        On failure:Raise Exception
        '''

        conn = self.dataBaseConnection(Database)
        Path =self.path
        onlyfiles = [f for f in listdir(Path)]
        log_file= open("Training_Logs/DBInsertLog.txt", 'a+')

        for file in onlyfiles:
            try:
                with open(Path+'/'+file,'r') as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO Raw_Data values ({values})'.format(values=(list_)))
                                self.logger.log(log_file, " %s: File loaded successfully!!" % file)
                                conn.commit()
                            except Exception as e:
                                raise e
            except Exception as e:
                conn.rollback()
                self.logger.log(log_file,"Error while creating table: %s"%e)
                log_file.close()
        conn.close()
        log_file.close()

    def selectingDatafromtableintocsv(self,Database):
        '''
                            Method Name:selectingDatafromtableintocsv
                            Description: This method exports the data in the GoodData table as a CSV file in a given location above created
                            Output: None
                            On Failier: Raise Exception
        '''

        self.fileFromDb= 'Training_FileFromDb/'
        self.fileName = 'Input.csv'
        log_file = open("Training_Logs/ExportToCsv.txt", 'a+')
        try:
            conn = self.dataBaseConnection(Database)
            sqlselect = "SELECT * FROM Raw_Data"
            cursor = conn.cursor()

            cursor.execute(sqlselect)

            results= cursor.fetchall()
            # GET the headers of the csv file
            headers = [i[0] for i in cursor.description]

            #Make the csv pit directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            #open CSV file for writing
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w',newline=''),delimiter=',',lineterminator='\r\n',quoting=csv.QUOTE_ALL,escapechar='\\')
            #Add the header and data to the CSV file
            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.logger.log(log_file, "File exported successfully!!!")
            log_file.close()

        except Exception as e:
            self.logger.log(log_file, "File exporting failed. Error : %s" % e)
            log_file.close()
            raise e

