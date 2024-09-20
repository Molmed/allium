import pandas as pd
import os
from gene_thesaurus import GeneThesaurus

gt = GeneThesaurus(data_dir='/tmp')

# TODO: make these command line parameters
# GEX data from Lilljebjorn et al. 2016
path_to_data = '/Users/marly389/Data/lilljebjorn/'
input_file = f'{path_to_data}/counts.raw.lilljebjorn.csv'
output_file = f'{path_to_data}/counts.filtered.lilljebjorn.csv'

# Reference
REFERENCE_GENOME = 'Homo_sapiens.GRCh38.103'
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, '../../data/reference')
ANNOT_FILE_FILTERED = os.path.join(
    DATA_DIR, (f'{REFERENCE_GENOME}.allium.annotations.filtered.csv'))

# Load the data
data = pd.read_csv(input_file, index_col=0)
ref = pd.read_csv(ANNOT_FILE_FILTERED)

# Convert all data values to float
data = data.astype('float64')

# TODO: add command-line parameters to determine if translation from ensembl id is necessary
# Get gene names from ensembl ids
# translated_genes = gt.translate_genes(data.index.values,
#                                       source='ensembl_id',
#                                       target='symbol')
# data['gene_name_std'] = data.index.map(translated_genes).fillna("")

# Get all gene name values to update to the latest standard
updated_genes = gt.update_gene_symbols(data.index.values)

# Copy data.index to gene_name_std
data['gene_name_std'] = data.index

# Update gene_name_std from updated_genes
data['gene_name_std'] = data['gene_name_std'].map(updated_genes).fillna(data['gene_name_std'])

# Do the same for ref
updated_genes = gt.update_gene_symbols(ref['name'].values)

# Set new column with the latest gene name
ref['gene_name_std'] = ref['name'].map(updated_genes).fillna(ref['name'])

# Drop all rows in data where gene_name_std does not appear in ref['gene_name_std']
data = data[data['gene_name_std'].isin(ref['gene_name_std'])]

# Join the two dataframes on the gene_name_std column
data = data.join(ref.set_index('gene_name_std'), on='gene_name_std')

# Get duplicates
duplicates = data[data['id'].duplicated(keep=False)]

# For each row in duplicates, sum the values of the rows with the same id
# and update the row with the sum. Then drop the duplicates.
case_columns = [col for col in duplicates.columns if col.startswith("Case")]
for idx, row in duplicates.iterrows():
    # Get all rows with the same id
    dupes = data[data['id'] == row['id']]

    # Sum the counts of the rows
    new_counts = dupes[case_columns].sum()

    # Update the corresponding data rows with the new counts
    data.loc[data['id'] == row['id'], case_columns] = new_counts.values

# Keep only the first record of all duplicates
data = data.drop_duplicates(subset='id')

# Print records in ref.id that are not in data.id
missing = ref[~ref['id'].isin(data['id'])]

# Drop all columns except for the case columns
data = data[case_columns]

# Create records for all missing genes in data, filled with 0s
# The missing$id is the index value, and all the case columns are 0
missing_data = pd.DataFrame(index=missing['name'], columns=case_columns, data=0)

# Remove index name
missing_data.index.name = None

# Append the missing data to the data
data = pd.concat([data, missing_data])

# Dump data to file
data.to_csv(output_file)
