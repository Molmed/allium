from .allium_classifier import AlliumClassifier
from .helpers import models_path, signatures_path
from .subtype import Subtype
from .modality import DNAM
import joblib
import pandas as pd

class DNAMClassifier(AlliumClassifier):
    def __init__(self, version="v1"):
        super().__init__(version)
        self._model = joblib.load(models_path(f'allium_dnam_{version}.joblib'))
        self._imputer = joblib.load(models_path(f'allium_dnam_imputation_{version}.joblib'))
        self._signatures = pd.read_csv(signatures_path(f'signature_cpgs_{version}.csv'))

    def predict(self, dnam):
        super().predict(dnam)
        self._predictions = self.predictionsNSC(subtype_groups = Subtype.all(DNAM),
                                                model = self._model,
                                                discoverydf = dnam,
                                                unique_genedf = self._signatures,
                                                subtypecol = 'Subtype',
                                                ids = 'TargetID',
                                                name = 'DNAm_subtype',
                                                datatype = 'DNAm',
                                                signature_mode = 'separate',
                                                imputation = self._imputer)
