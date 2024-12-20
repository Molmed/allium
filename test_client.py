import pandas as pd
from allium.helpers import data_path, app_path
from allium.gex_classifier import GEXClassifier
from allium.dnam_classifier import DNAMClassifier
import joblib
from pathlib import Path

def test_predict_gex():
    testX = pd.read_csv(data_path('gex/gex.csv', test_data=True), index_col="public_id")
    pheno = pd.read_csv(data_path('gex/pheno.csv', test_data=True), index_col="Sample SJ ID")
    gc = GEXClassifier('v3')
    return gc.get_predictions(testX, pheno=pheno, json=True)

def test_predict_dnam():
    testX = pd.read_csv(data_path('dnam/dnam_v2.csv', test_data=True), index_col="ID_REF")
    pheno = pd.read_csv(data_path('dnam/pheno.csv', test_data=True), index_col="public_id")
    dnamc = DNAMClassifier('v3')
    return dnamc.get_predictions(testX, pheno=pheno, json=True)
