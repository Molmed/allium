import pandas as pd
from src.allium.gex_classifier import GEXClassifier

datasets = ['jude', 'lilljebjorn', 'tran']
data_dir = '/home/mariya/Data/allium'
gc = GEXClassifier('v3')

for dataset in datasets:
    print("Predicting for", dataset)
    testX = pd.read_csv(f'{data_dir}/{dataset}.counts.allium.csv',
                        index_col="id")
    pheno = pd.read_csv(f'{data_dir}/{dataset}.pheno.allium.csv',
                        index_col="id",
                        sep=';')
    result = gc.get_predictions(testX, pheno=pheno)
    result.to_csv(f'{data_dir}/{dataset}.predictions.csv')
