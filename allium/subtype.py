from pathlib import Path
import yaml

class Subtype:
    _SUBTYPES_YML = str(Path(__file__).parent.absolute()) + '/conf/subtypes.yml'
    _subtypes = {}

    with open(_SUBTYPES_YML, 'r') as file:
        _subtypes = yaml.safe_load(file)

    @staticmethod
    def all(modality):
        # Try to get dict for specific modality,
        # if it doesn't exist just return the base dict
        try:
            return Subtype._subtypes[modality]
        except:
            return Subtype._subtypes["base"]
