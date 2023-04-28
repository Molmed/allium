import pandas as pd
from allium.helpers import data_path
from allium.dnam_classifier import DNAMClassifier

def test_dnam_predict():
    testX = pd.read_csv(data_path('dnam/dnam.csv', test_data=True), index_col="ID_REF")
    pheno = pd.read_csv(data_path('dnam/pheno.csv', test_data=True), index_col="public_id")
    dnamc = DNAMClassifier()
    dnamc.predict(testX, pheno)
