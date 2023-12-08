from .helpers import conf_path
import yaml


class Subtype:
    _SUBTYPES_YML = conf_path('subtypes.yml')
    _subtypes = {}

    with open(_SUBTYPES_YML, 'r') as file:
        _subtypes = yaml.safe_load(file)

    @staticmethod
    def all(modality):
        # Try to get dict for specific modality,
        # if it doesn't exist just return the base dict
        try:
            return Subtype._subtypes[modality]
        except KeyError:
            return Subtype._subtypes["base"]

    @staticmethod
    def group(subtype, modality):
        subtypes = Subtype.all(modality)
        for key, values in subtypes.items():
            if subtype in values:
                return key
        return subtype

    @staticmethod
    def groups(modality):
        return list(Subtype.all(modality).keys())

    @staticmethod
    def subtypes(modality):
        return [subtype for subtypes in
                Subtype.all(modality).values() for subtype in subtypes]
