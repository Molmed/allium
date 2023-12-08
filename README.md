# ALLIUM v1.0.0 :garlic:

## About

ALLIUM (ALL subtype Identification Using Machine learning) is a multimodal classifier of molecular subtypes in pediatric acute lymphoblastic leukemia, using DNA methylation (DNAm) and gene expression (GEX) data.

## Pre-requisites
Python 3.8+ and Conda

## Conda environment

You will need to activate the `allium` conda environment before running any subsequent commands.

Install: `conda env create -f environment.yml`

Activate: `conda activate allium`

Update (after changes to environment.yml): `conda env update --file environment.yml --prune`

## Prediction client
Run `python test_client.py` to run GEX and DNAm prediction on test datasets.

## Tests
Run `pytest`.

## Limitations

The models were trained using an older version of scikit-learn, due to some legacy dependency issues. This package, together with the Python version, should preferably be upgraded when retraining the model.
