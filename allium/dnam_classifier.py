from .allium_classifier import AlliumClassifier
from .helpers import models_path, signatures_path
from .subtype import Subtype
from .modality import DNAM
import joblib
import pandas as pd

class DNAMClassifier(AlliumClassifier):
    _DNAM_MODEL = models_path('allium_dnam_v1.joblib')
    _IMPUTATION_MODEL = models_path('allium_dnam_imputation_v1.joblib')
    _DNAM_SIGNATURES = signatures_path('signature_cpgs.csv')

    _model = joblib.load(_DNAM_MODEL)
    _imputer = joblib.load(_IMPUTATION_MODEL)
    _signatures = pd.read_csv(_DNAM_SIGNATURES)
    
    def predict(dnam_data):
        return 0
    
    def predictions(self, dnam, pheno):        
        return self.predictionsNSC(subtype_groups = Subtype.all(DNAM),
                            model = self._model, 
                            discoverydf = dnam, 
                            discoverypheno = pheno,
                            clinicaldatalist = ['Subtype_updated'],
                            unique_genedf = self._signatures, 
                            subtypecol = 'Subtype',
                            ids = 'TargetID',
                            name = 'DNAm_subtype',
                            datatype = 'DNAm',
                            signature_mode = 'separate', 
                            imputation = self._imputer)
