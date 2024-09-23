from sklearn.utils.extmath import softmax
from sklearn.metrics.pairwise import pairwise_distances

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
