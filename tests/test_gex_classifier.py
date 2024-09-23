import pandas as pd
from allium.helpers import data_path
from allium.gex_classifier import GEXClassifier

def test_gex_predict():
    testX = pd.read_csv(data_path('gex/gex.csv', test_data=True), index_col="public_id")
    pheno = pd.read_csv(data_path('gex/pheno.csv', test_data=True), index_col="Sample SJ ID")
    gc = GEXClassifier('v2')
    gc.get_predictions(testX, pheno=pheno)

