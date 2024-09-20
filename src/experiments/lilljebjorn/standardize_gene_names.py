
import pandas as pd

# GEX data from Lilljebjorn et al. 2016
path_to_data = '/Users/marly389/Data/lilljebjorn/'
input_file = f'{path_to_data}/BCP-ALL_expected_counts.csv'
output_file = f'{path_to_data}/counts.raw.lilljebjorn.csv'

# Load the data
data = pd.read_csv(input_file, index_col=0)

# Update index to use the gene name
data.index = data.index.str.split('_').str[1]

# Drop all rows whose index starts with "ENSGR", these are Y chr genes
# https://www.gencodegenes.org/pages/faq.html
data = data[~data.index.str.startswith("ENSGR")]

# Write to file
data.to_csv(output_file)
