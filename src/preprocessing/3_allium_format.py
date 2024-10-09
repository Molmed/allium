import pandas as pd

# TODO: make these command line parameters
# GEX data from tran et al. 2016
path_to_data = '/home/mariya/Data/tran/'
input_file = f'{path_to_data}/counts.norm.tran.csv'
output_file = f'{path_to_data}/counts.allium.tran.csv'

# Load the data
data = pd.read_csv(input_file, index_col=0)

# Format
data = data.T
data.index.name = 'public_id'
data.columns.name = None

# Dump to file
data.to_csv(output_file)
