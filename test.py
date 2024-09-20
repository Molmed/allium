import pandas as pd
from src.allium.gex_classifier import GEXClassifier

testX = pd.read_csv('/home/marly389-local/Development/data/counts.allium.lilljebjorn.csv', index_col="public_id")
gc = GEXClassifier('v2')
result = gc.predict(testX, None, to_json=False)
result.to_csv('/home/marly389-local/Development/data/predictions.lilljebjorn.csv')