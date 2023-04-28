from pathlib import Path
from sklearn.utils.extmath import softmax
from sklearn.metrics.pairwise import pairwise_distances

def base_path():
    return str(Path(__file__).parent.absolute())

def app_path(relative_path):
    return base_path() + '/' + relative_path

def data_path(relative_path, test_data=False):
    if test_data:
        relative_path = '/test_data/' + relative_path
    return base_path() + '/../data/' + relative_path

def conf_path(relative_path):
    return base_path() + '/../conf/' + relative_path

def models_path(relative_path):
    return data_path('/models/' + relative_path)

def signatures_path(relative_path):
    return data_path('/signatures/' + relative_path)

def predict_proba(self, X):
    
        """
        Arguments:
        
        --X: pandas dataframe num_samples x num_features for the dataset the predictions will be made on and calculate the distances
        
        Returns:
        
        --probs: prediction probabilities for each class for the samples in X
        """
        distances = pairwise_distances(X, self.centroids_, metric=self.metric)
        probs = softmax(-distances) # with the minus the highest probability score will be given to the class with the smallest distance
        return probs
