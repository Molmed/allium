
import pandas as pd
import os

# GEX data from https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE181157
data_path = '/home/mariya/Data/tran'
raw_data_path = f'{data_path}/GSE181157_RAW/'
output_file = f'{data_path}/counts.raw.tran.csv'

# Read all filenames in directory
files = os.listdir(raw_data_path)

dfs = {}
for filename in files:
    path = os.path.join(raw_data_path, filename)

    # The sample name is everything after the first underscore and before the period
    sample = filename.split('_', 1)[1].split('.')[0]

    # Convert space separated text file to df, use first col as index
    sample_df = pd.read_csv(path, sep='\t', header=None, index_col=0)

    # Remove index name
    sample_df.index.name = None

    # Call the other column "count"
    sample_df.columns = ['count']

    # Create a new column with the sample name
    dfs[sample] = sample_df['count']

# Concatenate all dataframes, using key as column name
data = pd.concat(dfs, axis=1)

# Sort columns by name
data = data.sort_index(axis=1)

# Drop all rows whose index starts with "__"
data = data[~data.index.str.startswith("__")]

# Write to file
data.to_csv(output_file)
