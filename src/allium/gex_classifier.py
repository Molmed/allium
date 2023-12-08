from .allium_classifier import AlliumClassifier
from .helpers import models_path, signatures_path
from .subtype import Subtype
from .modality import GEX
import joblib
import pandas as pd
import numpy as np

class GEXClassifier(AlliumClassifier):
    _model = joblib.load(models_path('allium_gex_v1.joblib'))
    _signatures = pd.read_csv(signatures_path('signature_genes.csv'))
    
    @staticmethod
    def preprocess_phenotypes(pheno):
        if pheno is None:
            return None
        pheno['Subtypes'] = [name.split('_')[0] for name in pheno.Subtype_name]
        pheno.Subtypes.replace(['ETV6-RUNX1', 'Hyperdiploid', 'DUX4-ERG'], ['t(12;21)', 'HeH', 'DUX4-r'], inplace = True)
        return pheno
    
    def predict(self, gex, pheno = None, to_json = False):
        return self.predictionsNSC(subtype_groups = Subtype.all(GEX),
                            model = self._model, 
                            discoverydf = gex, 
                            discoverypheno = GEXClassifier.preprocess_phenotypes(pheno),
                            clinicaldatalist = ['Subtypes'] if not pheno is None else None,
                            unique_genedf = self._signatures, 
                            subtypecol = 'Subtype',
                            ids = 'Gene ID',
                            name = 'GEX_subtype',
                            datatype = 'GEX',
                            signature_mode = 'all',
                            to_json=to_json)

            

