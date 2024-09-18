# ALLIUM v2.0.0 :garlic:

## About

ALLIUM (ALL subtype Identification Using Machine learning) is a multimodal classifier of molecular subtypes in pediatric acute lymphoblastic leukemia, using DNA methylation (DNAm) and gene expression (GEX) data. The reference genome used by this model is Homo_sapiens.GRCh38.103.

## Modules

This repository contains:
- the ALLIUM models
- GEX and DNAm prediction clients
- data preprocessing helpers
- metadata generation helpers (use only if changing reference genome versions)
- test data

## Pre-requisites
General:
- Python 3.8+
- Conda

For regenerating metadata for a different reference genome:
- R 4.4.1 or later, and renv

You may need to install additional libraries depending on your operating system.

## Conda environment
You will need to activate the `allium` conda environment before running any subsequent commands.

Install: `conda env create -f environment.yml`

Activate: `conda activate allium`

Update (after changes to environment.yml): `conda env update --file environment.yml --prune`

## R Environment (for preprocessing data files only)
Start R from the project directory, then run: `renv::restore()`

## Prediction client
Run `python test_client.py` to run GEX and DNAm prediction on test datasets.

## Tests
Run `pytest`.

## Limitations
The models were trained using an older version of scikit-learn, due to some legacy dependency issues. This package, together with the Python version, should preferably be upgraded when retraining the model. Due to this, the current version of the prediction client does not work on Mac OS.
