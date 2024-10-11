import pandas as pd
from src.allium.gex_classifier import GEXClassifier

testX = pd.read_csv('/home/mariya/Data/tran/counts.allium.tran.csv', index_col="public_id")
pheno = pd.read_csv('/home/mariya/Data/tran/pheno.allium.tran.csv', index_col = "public_id")

gc = GEXClassifier('v3')

result = gc.get_predictions(testX, pheno=pheno)
result.to_csv('/home/mariya/Data/tran/predictions.tran.csv')
