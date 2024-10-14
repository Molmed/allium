import pandas as pd
import os
import re
from gene_thesaurus import GeneThesaurus


class Preprocessor():
    def __init__(self,
                 prefix,
                 input_file,
                 output_dir,
                 gene_format,
                 sample_col_regex,
                 ref_data_dir=None,
                 ref_genome='Homo_sapiens.GRCh38.103',
                 tmp_dir='/tmp'):

        self._input_file = input_file
        # TODO: CHANGE
        # self._output_file_path = f'{output_dir}/{prefix}.counts.allium.csv'
        self._output_file_path = f'{output_dir}/{prefix}.counts.filtered.csv'

        # Throw exception if gene_format is not 'symbol' or 'ensembl'
        if gene_format not in ['symbol', 'ensembl']:
            raise ValueError(
                'gene_format must be either "symbol" or "ensembl"')
        self._gene_format = gene_format
        self._sample_col_regex = sample_col_regex

        # If not ref data dir, use the local one
        if not ref_data_dir:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            ref_data_dir = os.path.join(script_dir, '../../data/reference')
        self._annot_file_filtered = os.path.join(
            ref_data_dir, (f'{ref_genome}.allium.annotations.filtered.csv'))

        self._gt = GeneThesaurus(data_dir=tmp_dir)

    def run(self):
        self._preprocess_genes()

    def _preprocess_genes(self):
        # Load the data
        data = pd.read_csv(self._input_file, index_col=0)
        ref = pd.read_csv(self._annot_file_filtered)

        if self._gene_format == 'ensembl':
            # Get gene names from ensembl ids
            translated_genes = self._gt.translate_genes(data.index.values,
                                                        source='ensembl_id',
                                                        target='symbol')
            data['gene_name_std'] = data.index.map(translated_genes).fillna("")
        else:
            # Code to use if index is in symbol format
            # Get all gene name values to update to the latest standard
            updated_genes = self._gt.update_gene_symbols(data.index.values)

            # Copy data.index to gene_name_std
            data['gene_name_std'] = data.index

            # Update gene_name_std from updated_genes
            data['gene_name_std'] = data['gene_name_std'].map(
                updated_genes).fillna(data['gene_name_std'])

        # Do the same for ref
        updated_genes = self._gt.update_gene_symbols(ref['name'].values)

        # Set new column with the latest gene name
        ref['gene_name_std'] = ref['name'].map(
            updated_genes).fillna(ref['name'])

        # Drop all rows in data where gene_name_std
        # does not appear in ref['gene_name_std']
        data = data[data['gene_name_std'].isin(ref['gene_name_std'])]

        # Join the two dataframes on the gene_name_std column
        data = data.join(ref.set_index('gene_name_std'), on='gene_name_std')

        # Get duplicates
        duplicates = data[data.duplicated(subset='gene_name_std', keep=False)]

        # Get all unique indices from duplicates
        duplicate_gene_names = duplicates['gene_name_std'].unique()

        # For each row in duplicates,
        # sum the values of the rows with the same name
        # and update the row with the sum. Then drop the duplicates.
        case_columns = [col for col in duplicates.columns if
                        re.match(self._sample_col_regex, col)]

        for duplicate_gene in duplicate_gene_names:
            # Get all rows with the same id
            dupes = data[data['gene_name_std'] == duplicate_gene]

            # Sum the rows
            new_counts = dupes[case_columns].sum()

            # Update the corresponding data rows with the new counts
            data.loc[
                data['gene_name_std'] == duplicate_gene, case_columns
                ] = new_counts.values

        # Keep only the first record of all duplicates
        data = data.drop_duplicates(subset='gene_name_std')

        # Print records in ref.id that are not in data.id
        missing = ref[~ref['id'].isin(data['id'])]

        # Change index to id column
        data = data.set_index('id')

        # Drop all columns except for the case columns
        data = data[case_columns]

        # Create records for all missing genes in data, filled with 0s
        # The missing$id is the index value, and all the case columns are 0
        missing_data = pd.DataFrame(index=missing['id'],
                                    columns=case_columns,
                                    data=0)

        # Remove index name
        missing_data.index.name = None

        # Append the missing data to the data
        data = pd.concat([data, missing_data])

        # Sort data by index
        data = data.sort_index()

        # Dump data to file
        data.to_csv(self._output_file_path)
