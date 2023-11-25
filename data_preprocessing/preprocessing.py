import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


class Preprocessor:
    '''
                this class shall be used to clean and transform the data before training.
    '''

    def __init__(self,file_object,logger_object):
        self.file_object= file_object
        self.logger_object = logger_object

    def remove_columns(self,data,columns):
        '''
                        Method Name: remove_columns
                        Description: This method removes the given columns from a pandas dataframe.
                        Output: A pandas DataFrame after removing the specified columns.
                        On Failure: Raise Exception
        '''
        self.logger_object.log(self.file_object, 'Entered the remove_columns method of the preprocessor class')
        self.data=data
        self.columns=columns
        try:
            #drop the labels specified in the columns
            self.useful_data=self.data.drop(labels=self.columns,axis=1)
            self.logger_object.log(self.file_object,'Column removal Successful.Exited the remove_columns method of the Preprocessor class')
            return self.useful_data

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in remove_columns method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,'Column removal Unsuccessful. Exited the remove_columns method of the Preprocessor class')
            raise Exception()

    def separate_label_feature(self,data,label_column_name):
        '''
                                Method Name: seprate_label_feature
                                Description: This method separeates the features and a label columns
                                Output: Returns two seperate Dataframe, one containing features and the other containing Labels.
                                On Failure: Raise Exception
        '''
        self.logger_object.log(self.file_object,'Entered the seperate_label_feature method of the preprocessing class')
        try:
            #drop the columns specified and seprate the feature columns
            self.x=data.drop(labels=label_column_name,axis=1)
            #Filter the label column
            self.y = data[label_column_name]
            self.logger_object.log(self.file_object,'Label seperation Succesfull. Exited the seperate_label feature method od the preproccessor class')
            return self.x,self.y
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in separate_label_feature method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Label Separation Unsuccessful. Exited the separate_label_feature method of the Preprocessor class')
            raise Exception()

    def dropUnnecessaryColumns(self,data,columnNameList):
        '''
                                Method Name: dropUnnecessaryColumns
                                Description: This method drops the unwanted columns as discussed in the EDA section.
                                Output: Returns data after dropping unneccessary columns

        '''

        data = data.drop(columnNameList,axis=1)
        return data
    def replaceInvalidValuesWithNull(self,data):
        '''
                                Method Name: replaceInvalidValuesWithNull
                                Description: This method replaces invalid values i.e. '?' with null,as discussed in EDA
                                Output: Returns data after replacing invalid values with Null
        '''

        for column in data.columns:
            count=data[column][data[column] == '?'].count()
            if count != 0:
                data[column] = data[column].replace('?',np.nan)
        return data
    def is_null_present(self,data):
       '''
                    Method Name: is_null_present
                    Description: This method checks wheter there are null values present in the pandas DataFrame or not.
                    Output: Returns True if null values are present in the DataFrame,False if they are not present and returns the list of columns for which null values are present.
                    On Failure: Raise Exception
       '''

       self.logger_object.log(self.file_object, 'Entered the is_null_present method of the Preprocessor class')
       self.null_present= False
       self.cols_with_missing_values=[]
       self.cols = data.columns
       try:
           # check for the count of null values per column
           self.null_counts = data.isna().sum()
           for i in range(len(self.null_counts)):
               if self.null_counts[i]>0:
                   self.null_present=True
                   self.cols_with_missing_values.append(self.cols[i])
           #Write the Logs to see which columns have null values
           if(self.null_present):
               self.dataframe_with_null = pd.DataFrame()
               self.dataframe_with_null['columns'] = data.columns
               self.dataframe_with_null['missing values count']= np.asarray(data.isna().sum())
               # storing the null column information to file
               self.dataframe_with_null.to_csv('preprocessing_data/null_values.csv')
           self.logger_object.log(self.file_object,'Finding missing values is a success.Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
           return self.null_present, self.cols_with_missing_values
       except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in is_null_present method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Finding missing values failed. Exited the is_null_present method of the Preprocessor class')
            raise Exception()

    def scale_numerical_columns(self,data):
        """
                                                        Method Name: scale_numerical_columns
                                                        Description: This method scales the numerical values using the Standard scaler.
                                                        Output: A dataframe with scaled
                                                        On Failure: Raise Exception

                                     """
        self.logger_object.log(self.file_object,
                               'Entered the scale_numerical_columns method of the Preprocessor class')

        self.data=data

        try:
            self.num_df = self.data.select_dtypes(include=['int64']).copy()
            self.scaler = StandardScaler()
            self.scaled_data = self.scaler.fit_transform(self.num_df)
            self.scaled_num_df = pd.DataFrame(data=self.scaled_data, columns=self.num_df.columns)


            self.logger_object.log(self.file_object, 'scaling for numerical values successful. Exited the scale_numerical_columns method of the Preprocessor class')
            return self.scaled_num_df

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in scale_numerical_columns method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'scaling for numerical columns Failed. Exited the scale_numerical_columns method of the Preprocessor class')
            raise Exception()

    def get_columns_with_zero_std_deviation(self, data):
        '''
                                                Method Name: get_columns_with_zero_std_deviation
                                                Description: This method finds out the columns which have a standard deviation of zero.
                                                Output: List of the columns with standard deviation of zero
                                                On Failure: Raise Exception

        '''
        self.logger_object.log(self.file_object,
                               'Entered the get_columns_with_zero_std_deviation method of the Preprocessor class')
        self.columns = data.columns
        self.data_n = data.describe()
        self.col_to_drop = []
        try:
            for x in self.columns:
                if (self.data_n[x]['std'] == 0):  # check if standard deviation is zero
                    self.col_to_drop.append(x)  # prepare the list of columns with standard deviation zero
            self.logger_object.log(self.file_object,
                                   'Column search for Standard Deviation of Zero Successful. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            return self.col_to_drop

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_columns_with_zero_std_deviation method of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'Column search for Standard Deviation of Zero Failed. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            raise Exception()