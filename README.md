# ALLIUM v2.2.0 :garlic:

## About

ALLIUM (ALL subtype Identification Using Machine learning) is a multimodal classifier of molecular subtypes in pediatric acute lymphoblastic leukemia, using DNA methylation (DNAm) and gene expression (GEX) data. The reference genome used by this model is Homo_sapiens.GRCh38.103.

### Publication

Krali, O., Marincevic-Zuniga, Y., Arvidsson, G. et al. Multimodal classification of molecular subtypes in pediatric acute lymphoblastic leukemia. npj Precis. Onc. 7, 131 (2023). https://doi.org/10.1038/s41698-023-00479-5

## Modules

This repository contains:
- the ALLIUM models
- GEX and DNAm prediction clients
- test data

## Conda environment
[Conda](https://docs.conda.io) must be installed on your system.

You will need to activate the `allium` conda environment before running any subsequent commands.

Install: `conda env create -f environment.yml`

Activate: `conda activate allium`

Update (after changes to environment.yml): `conda env update --file environment.yml --prune`

## Prediction client
Run `python test_client.py` to run GEX and DNAm prediction on test datasets.

## Tests
Run `pytest`.

## Preprocessing GEX data
Preprocessing tools are available in the [ALLIUM PrePro](https://github.com/Molmed/allium_prepro) repository.

## Limitations
The models were trained using an older version of scikit-learn, due to some legacy dependency issues. This package, together with the Python version, should preferably be upgraded when retraining the model. Due to this, the current version of the prediction client does not work on Mac OS.
