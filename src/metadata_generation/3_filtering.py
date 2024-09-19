import os
import pandas as pd

REFERENCE_GENOME = 'Homo_sapiens.GRCh38.103'

# Define the directory to save the file relative to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, '../../data/reference')
ANNOT_FILE = os.path.join(DATA_DIR, (f'{REFERENCE_GENOME}.allium.annotations.full.csv'))
ANNOT_FILE_FILTERED = os.path.join(
    DATA_DIR, (f'{REFERENCE_GENOME}.allium.annotations.filtered.csv'))

# Read in file
annot = pd.read_csv(ANNOT_FILE)

# Get all rows where biotype is protein_coding
protein_coding_annot = annot.loc[annot['biotype'] == 'protein_coding']

# Only keep genes that are on chrs 1-22 and X
valid_chromosomes = [str(i) for i in range(1, 23)] + ['X']

# Keep only genes where chr is in valid_chromosomes
filtered_annot = protein_coding_annot[
    protein_coding_annot['chr'].isin(valid_chromosomes)]

# Remove ribosomal genes
filtered_annot = filtered_annot[
    ~filtered_annot['name'].str.startswith(('RPL', 'RPS'))]

# Write the filtered DataFrame to a CSV file
filtered_annot.to_csv(ANNOT_FILE_FILTERED, index=False)
