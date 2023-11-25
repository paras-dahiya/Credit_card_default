
from datetime import datetime
import os
import re
import json
import shutil
import pandas as pd
from Application_logging.logger import App_logger

class Raw_Data_validation:

    '''
    This class shall be used for handling all the validation done on the Raw Training
    Data!!.
    '''


    def __init__(self,path):
        self.Batch_Directory = path
        self.schema_path ='schema_training.json'
        self.logger = App_logger()

    def valuesFromSchema(self):

       '''
                Method Name : valuesFromSchema
                Description : This method extracts all the relevent information from the predined "Schema" file.
                Output : column_names, Number of columns
                On Failure : Raise ValueError, KeyError,Exception
         '''
       try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
                f.close()
            column_names = dic['ColName']
            noofcolumns = dic['NumberofColumns']

            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            message ="NumberofColumns:: %s" %noofcolumns + "\n"
            self.logger.log(file,message)
            file.close()


       except ValueError:
            file=open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file,"ValueError:Value not found inside schema_training.json")
            file.close()
            raise ValueError

       except KeyError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, "KeyError:Key value error incorrect key passed")
            file.close()
            raise KeyError

       except Exception as e:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise e
       return column_names, noofcolumns
