import pandas as pd
from allium.helpers import data_path, app_path
from allium.gex_classifier import GEXClassifier
from allium.dnam_classifier import DNAMClassifier
import joblib
from pathlib import Path

def test_predict_gex():
    testX = pd.read_csv(data_path('gex/gex.csv', test_data=True), index_col="public_id")
    pheno = pd.read_csv(data_path('gex/pheno.csv', test_data=True), index_col="Sample SJ ID")
    gc = GEXClassifier()
    return gc.predictions(testX, pheno)

def test_predict_dnam():
    testX = pd.read_csv(data_path('dnam/dnam.csv', test_data=True), index_col="ID_REF")
    pheno = pd.read_csv(data_path('dnam/pheno.csv', test_data=True), index_col="public_id")
    dnamc = DNAMClassifier()
    return dnamc.predictions(testX, pheno)

#print()
test_predict_gex()


# path = app_path('../legacy/test_data/DNAm/DNAm_test_v2.pkl')
# testX =  joblib.load(path)

# testX.to_csv(data_path("dnam/dnam.csv", test_data=True), index_label="ID_REF")

# path = app_path('../legacy/test_data/DNAm/DNAm_pheno_test.pkl')
# testpheno = joblib.load(path)
# testpheno.to_csv(data_path("dnam/pheno.csv", test_data=True), index_label="public_id")

# print(testX)
# print(testpheno)
