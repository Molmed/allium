import pandas as pd
import yaml
import os

# GEX data from Lilljebjorn et al. 2016
path_to_data = '/Users/marly389/Data/lilljebjorn/'
input_file = f'{path_to_data}/pheno.lilljebjorn.csv'
output_file = f'{path_to_data}/pheno.allium.lilljebjorn.csv'

# Get current script path
script_dir = os.path.dirname(os.path.abspath(__file__))
subtypes_file = f'{script_dir}/subtypes_to_allium.yml'

# Load the data
data = pd.read_csv(input_file, index_col=0, sep=';')

# Get subtype translation
with open(subtypes_file, 'r') as f:
    subtypes_dict = yaml.safe_load(f)

# Replace Subtype column using dict
data['Subtype'] = data['Subtype'].replace(subtypes_dict)

# Dumop to output file
data.to_csv(output_file)
