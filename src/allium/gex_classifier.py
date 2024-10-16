from .allium_classifier import AlliumClassifier
from .helpers import models_path, signatures_path
from .subtype import Subtype
from .modality import GEX
import joblib
import pandas as pd


class GEXClassifier(AlliumClassifier):
    def __init__(self, version="v1"):
        super().__init__(version)
        self._model = joblib.load(models_path(f'allium_gex_{version}.joblib'))
        self._signatures = pd.read_csv(signatures_path(f'signature_genes_{version}.csv'))

    def predict(self, gex):
        super().predict(gex)
        self._predictions = self.predictionsNSC(subtype_groups = Subtype.all(GEX),
                                                model = self._model,
                                                discoverydf = gex,
                                                unique_genedf = self._signatures,
                                                subtypecol = 'Subtype',
                                                ids = 'Gene ID',
                                                name = 'GEX_subtype',
                                                datatype = 'GEX',
                                                signature_mode = 'all')

    def get_predictions(self, x, pheno=None, json=False):
        self.predict(x)
        return super().get_predictions(x, pheno, json)
