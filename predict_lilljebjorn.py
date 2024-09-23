import pandas as pd
from src.allium.gex_classifier import GEXClassifier

testX = pd.read_csv('/home/marly389-local/Development/data/counts.allium.lilljebjorn.csv', index_col="public_id")
pheno = pd.read_csv('/home/marly389-local/Development/data/cpheno.allium.lilljebjorn.csv', index_col = "public_id")


gc = GEXClassifier('v2')
result = gc.predict(testX, pheno, to_json=False, known_subtype_col='Subtype')
result.to_csv('/home/marly389-local/Development/data/predictions.lilljebjorn.csv')
