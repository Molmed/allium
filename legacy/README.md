#### A) You need to create a conda environment as follows (use the .yml file that is provided):

+ conda env create -f environment.yml - this file has a premade environment name 'myenv'. You can change it at your convenience 

#### B) Alteratively 

+ conda create -n myenv python=3.8.5
+ conda activate myenv
+ pip install matplotlib==3.1.2
+ pip install pandas==1.1.5
+ pip install scikit-learn==0.23.2
+ pip install seaborn==0.11.1

##### A few more packages to install 

To add your enviroment on the jupyter notebook kernels you need to do the following:
+ conda activate myenv
+ pip install notebook
+ conda install ipykernel
+ python -m ipykernel install --user --name myenv --display-name "PickAName"

You are ready to :rocket:

#### To run a Jupyter notebook with R, you can create an R environment using the Anaconda navigator
---


## Folders included :file_folder:

1. ALLIUM_models: DNAm and GEX ALLIUM trained models are saved in a pickle (pkl) format. An imputer pickle file is provided for missing data imputation for the DNAm data

2. ALLIUM_signatures: The 519 CpG sites and 425 genes selected by the initial feature selection step by ALLIUM that are used to train the model and for subtype prediction

3. Notebooks_GEX_preprocessing: Jupyter notebooks for GEX data preprocessing for data that were not aligned to our reference genome version (Python), as well as and RNA sequencing data normalization (R)(see &#8595; Data format & preproccecing for new cases)

4. Notebooks_predictions: Jupyter notebooks with a walk-through for subtype prediction using public DNAm or GEX datasets. Construction of fusion matrix is included

5. outputs: The predictions from 4 are stored here by default in a csv format

6. test_data: The public DNAm (GSE56600; 227 pediatric B-cell ALL samples ([Lee et al., 2015](https://doi.org/10.1093/nar/gkv103))) and GEX (GSE16150; 19 pediatric B-cell ALL samples ([Diedrich et al., 2021](https://doi.org/10.1038/s41375-021-01209-1))) datasets used for 4

7. Train_Predict_modules: python modules used for ALLIUM's train/predict procedures that are utilized by the notebooks in 4 (see &#8595; Subtype prediction)

---


## Data format & preproccecing for new cases :card_file_box:
### DNAm (Illumina 450K array or EPIC array data are compatible)

+ The dataset should be in a dataframe format with samples as rows and CpG sites as columns
+ No further pre-processing is required (unless you need to correct for batch effects)
+ You can add information from a phenotype file if applicable, otherwise set the clinicaldatalist argument of the predictionsNSC as []



### GEX
+ Batch effects were corrected in our GEX dataset with the help of the R library [Combat-Seq](https://github.com/zhangyuqing/ComBat-seq). Input data as dataframe with genes as rows and samples as columns
+ Gene filtering was applied as described in our manuscript to result in [19,777 genes](./Notebooks_GEX_preprocessing/data/) for downstream analysis
+ GeTMM (Gene length corrected TMM) normalization was applied in R according to [Smid et al.](https://doi.org/10.1186/s12859-018-2246-7)(2018), allowing adjustment for gene length and library size. Input data as dataframe with genes as rows and samples as columns
+ All counts were log2 transformed prior to the train/prediction step
+ The dataset should be in a dataframe format with samples as rows and genes as columns
+ You can add information from a phenotype file if applicable, otherwise set the clinicaldatalist argument of the predictionsNSC as []

#### GEX predictions on test data aligned to a different version of reference genome

+ **Our GEX model was aligned to the GRCh38.103 reference genome (60,666 genes), however our test dataset was lifted from hg19 to our version**
+ **No batch effects were present, however if they are batch effects, you can correct from batch effects prior to the next steps.**
+ **Follow a walk-through in the folder Notebook_GEX_preprocessing to see how we proceeded with the test data, in case you have your data aligned in another version of the reference genome (including GeTMM and log2 transformation in R)**
+ **ENSEMBL IDs are the only input to ALLIUM GEX, use the [annotateddata.7z](./Notebooks_GEX_preprocessing/data/) if needed (unpack first)**


---

## Subtype prediction :question: :ballot_box_with_check:

Patient subtype prediction can work with two ways
+ **Use the notebooks from 4. Notebooks_predictions (&#8593;) with the test data as input or adjust them accordingly for your data.**

---
## Prediction columns explanation
+ Groups: groups with multiple subtypes (>=2) or single subtypes
+ Subtypes: single subtype entities
#### The prediction step works as follows:
+ During the first phase, group predictions are obtained ('data_type'_subtype), which can be either no class, single or multi-class. 
+ For the multi-class cases the Subtype detailed_v1 and Probability detailed_v1 reveal the predictions and scores for each group. 
+ Based on these scores a multi-to single class transformation will take place based on the group with the highest probability score.
+ Then for the winner group, the subtype that was predicted (datatype'_probability_V2) is selected and it's probability score is available ('datatype'_probability_V2).
+ Applied thresholds allow manual investigation of patient subtype with other molecular information for further verification.

<br>


| Column | Explanation |
| --- | --- |
| First columns | Defined by clinicaldatalist provided during the prediction step (clinicaldatalist can also be empty [])|
| columns ending with .classifier.proba | classifier probability per group/subtype: if the subtype proba is NA then the group proba score is <0.5|
| #predicted.classes | can be 0, 1 or >1 (multiclass) |
|'datatype'_subtype | can be no_class, single group class, multiclass|
| Subtype detailed_v1 | detailed subtype information that reveals multiclass cases|
| Probability detailed_v1 | detailed subtype probability scores that reveal multiclass cases|
|'datatype'_subtype_groups | group selected after multi-to single class transformation (highest probability_V1 score)|
|'#classes.updated | can be 0 or 1|
|'datatype'_probability_V2 | probability score of the selected subtype member|
|'datatype'_subtype_V2 | subtype prediction|
|'datatype'_subtype_comments | no class prediction (probability_V2 <0.5), manual check is required (0.5 <= probability_V2 <0.7), passed control (probability_V2 >=0.7)|


+ datatype can be replaced with either DNAm or GEX depending on the data used

