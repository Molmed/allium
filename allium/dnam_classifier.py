from .allium_classifier import AlliumClassifier
from .helpers import models_path, signatures_path
from .subtype import Subtype
from .modality import DNAM
import joblib
import pandas as pd

class DNAMClassifier(AlliumClassifier):
    _model = joblib.load(models_path('allium_dnam_v1.joblib'))
    _imputer = joblib.load(models_path('allium_dnam_imputation_v1.joblib'))
    _signatures = pd.read_csv(signatures_path('signature_cpgs.csv'))
    
    def predict(self, dnam, pheno):        
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
