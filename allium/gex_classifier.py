from .helpers import models_path
import joblib

class GEXClassifier():
    _GEX_MODEL = models_path('allium_gex_v1.joblib')
    _model = joblib.load(_GEX_MODEL)
    print(_model)
    
    def predict(gex_data):
        return 0
