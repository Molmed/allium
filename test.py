import pandas as pd
from allium.helpers import data_path
from allium.gex_classifier import GEXClassifier

def test_predict():
    testX = pd.read_csv(data_path('gex/gex.csv', test_data=True))
    pheno = pd.read_csv(data_path('gex/pheno.csv', test_data=True))
    gc = GEXClassifier()
    return gc.predictionsNSC(testX)

print(test_predict())
