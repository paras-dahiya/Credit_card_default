import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from file_operations import file_methods

class KMeansClustering:
    '''
            This class shall be used to divide the data into clusters before training
    '''
    def __init__(self,file_object,logger_object):
        self.file_object = file_object
        self.logger_object = logger_object

    def elbow_plot(self,data):
        '''
                            Method Name: elbow_plot
                            Description: This method save the plot to decide the optimum number of clusters to the file.
                            Output: A picture saved to the directory
                            On Failure: Raise Exception
        '''
        self.logger_object.log(self.file_object, 'Entered the elbow_plot method of the KMeansClustering class')
        #initalizing an empty list
        wcss = []
        try:
            for i in range(1,11):
                kmeans=KMeans(n_clusters=i,init='k-means++',random_state=42)  #initializing the k_means object
                kmeans.fit(data) # fitting the data to the KMeans Algorithm
                wcss.append(kmeans.inertia_)
            #Creating the graph between WCSS and the number of cluster
            plt.plot(range(1,11),wcss)
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel("WCSS")
            #for showing graph
            #plt.show()
            #saving the elbow plot locally
            plt.savefig('preprocessing_data/K-Means_Elbow.PNG')

            #Finding the value of the optium cluster programmatically
            self.kn = KneeLocator(range(1,11),wcss,curve='convex',direction='decreasing')
            self.logger_object.log(self.file_object, 'The optimum number of clusters is: ' + str(self.kn.knee) + ' . Exited the elbow_plot method of the KMeansClustering class')
            return self.kn.knee
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in elbow_plot method of the KMeansClustering class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Finding the number of clusters failed. Exited the elbow_plot method of the KMeansClustering class')
            raise Exception()

    def create_clusters(self,data,number_of_clusters):
        '''
                                    Method Name: create_clusters
                                    Description: Create a new dataframe consisting of cluster infromation
                                    Output: A dataframe with cluster column
                                    On Failure: Raise Exception
        '''
        self.logger_object.log(self.file_object, 'Entered the create_clusters method of the KMeansClustering class')
        self.data = data
        try:
            self.kmeans = KMeans(n_clusters=number_of_clusters,init='k-means++',random_state=42)
            #divide data into clusters
            self.y_kmeans=self.kmeans.fit_predict(data)
            self.file_op = file_methods.File_Operation(self.file_object,self.logger_object)
            #saving the KMeans model to directory
            self.save_model = self.file_op.save_model(self.kmeans,'KMeans')

            #create new column in dataset for storing the cluster information
            self.data['Cluster']=self.y_kmeans
            self.logger_object.log(self.file_object, 'succesfully created ' + str(self.kn.knee) + 'clusters. Exited the create_clusters method of the KMeansClustering class')
            return self.data

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in create_clusters method of the KMeansClustering class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Fitting the data to clusters failed. Exited the create_clusters method of the KMeansClustering class')
            raise Exception()