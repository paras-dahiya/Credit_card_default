import pandas
from Application_logging import logger
from file_operations import file_methods
from data_preprocessing import preprocessing

class prediction:

    def __init__(self):
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_logger()


    def predictFromModel(self,data):

        try:
            """doing the data preprocessing"""

            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)

            # Removing the id column
            #data = preprocessor.remove_columns(data, ['ID'])

            # check if missing values are present in the dataset
            is_null_present, cols_with_missing_values = preprocessor.is_null_present(data)

            file_loader = file_methods.File_Operation(self.file_object, self.log_writer)
            kmeans = file_loader.load_model('KMeans')

            clusters = kmeans.predict(data)
            data['clusters'] = clusters
            clusters = data['clusters'].unique()
            result = []

            for i in clusters:
                cluster_data = data[data['clusters'] == i]
                cluster_data = cluster_data.drop(['clusters'], axis=1)
                model_name = file_loader.find_correct_model_file(i)
                model = file_loader.load_model(model_name)
                for val in (model.predict(cluster_data)):
                    result.append(val)
                result = result[0]
            self.log_writer.log(self.file_object, 'End of Prediction')
        except Exception as ex:
            self.log_writer.log(self.file_object, 'Error occured while running the prediction!! Error:: %s' % ex)
            raise ex

        return result