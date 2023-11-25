from datetime import datetime
from DataTypeValidation_Insertion_Training.DataTypeValidation import dBOperation
from Application_logging import logger
from Training_Raw_data_validation.raw_validation import Raw_Data_validation
import os

class train_validation:
    def __init__(self,path):
        self.raw_data = Raw_Data_validation(path)
        self.dBOperation = dBOperation()
        self.cwd = os.getcwd()
        self.file_object = open("Training_Logs/Training_Main_Log.txt",'a+')
        self.log_writer = logger.App_logger()

    def train_validation(self):
        try:
            # extracting values from prediction schema
            column_names, noofcolumns = self.raw_data.valuesFromSchema()
            self.log_writer.log(self.file_object, 'Start of Validation on files for Training')
            self.log_writer.log(self.file_object,
                                "Creating Training_Database and tables on the basis of given schema!!!")
            # create database with given name, if present open the connection! Create table with columns given in schema
            self.dBOperation.createTableDb('Training', column_names)
            self.log_writer.log(self.file_object, "Table creation Completed!!")
            self.log_writer.log(self.file_object, "Insertion of Data into Table started!!!!")
            # insert csv files in the table
            self.dBOperation.insertIntoTable('Training')
            self.log_writer.log(self.file_object, "Insertion in Table completed!!!")
            self.log_writer.log(self.file_object, "Validation Operation completed!!")
            self.log_writer.log(self.file_object, "Extracting csv file from table")
            # export data in table to csvfile
            self.dBOperation.selectingDatafromtableintocsv('Training')
            self.file_object.close()

        except Exception as e:
            raise e