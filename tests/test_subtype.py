from allium.subtype import Subtype
from allium.modality import GEX, DNAM


def test_list():
    legacy_dnam_subtype_groups = {'aneuploidy': ['high hyperdiploid', 'low hyperdiploid', 'iAMP21', 'hypodiploid'], 'ph-group': ['BCR::ABL1', 'BCR::ABL1-like'],
                     'ETV6-group': ['ETV6::RUNX1', 'ETV6::RUNX1-like'],  'T-ALL': ['T-ALL'], 'DUX4-r': ['DUX4-r'],
           'PAX5alt': ['PAX5alt'], 'KMT2A-r': ['KMT2A-r'], 'ZNF384-r': ['ZNF384-r'], 'TCF3::PBX1': ['TCF3::PBX1'],
            'MEF2D-r':['MEF2D-r'], 'PAX5 P80R': ['PAX5 P80R'], 'NUTM1-r': ['NUTM1-r'], 'Control': ['Control']}

    legacy_gex_subtype_groups = {'aneuploidy': ['high hyperdiploid', 'low hyperdiploid', 'iAMP21'], 'ph-group': ['BCR::ABL1', 'BCR::ABL1-like'],
                     'ETV6-group': ['ETV6::RUNX1', 'ETV6::RUNX1-like'],  'T-ALL': ['T-ALL'], 'DUX4-r': ['DUX4-r'],
           'PAX5alt': ['PAX5alt'], 'KMT2A-r': ['KMT2A-r'], 'ZNF384-r': ['ZNF384-r'], 'TCF3::PBX1': ['TCF3::PBX1'],
            'MEF2D-r':['MEF2D-r'], 'PAX5 P80R': ['PAX5 P80R'], 'NUTM1-r': ['NUTM1-r'], 'Control': ['Control']}

    assert Subtype.all(GEX) == legacy_gex_subtype_groups
    assert Subtype.all(DNAM) == legacy_dnam_subtype_groups


def test_group():
    assert Subtype.group('high hyperdiploid', GEX) == 'aneuploidy'
    assert Subtype.group('high hyperdiploid', DNAM) == 'aneuploidy'
    assert Subtype.group('BCR::ABL1', GEX) == 'ph-group'
    assert Subtype.group('BCR::ABL1', DNAM) == 'ph-group'
    assert Subtype.group('ETV6::RUNX1', GEX) == 'ETV6-group'
    assert Subtype.group('ETV6::RUNX1', DNAM) == 'ETV6-group'
    assert Subtype.group('T-ALL', GEX) == 'T-ALL'
    assert Subtype.group('T-ALL', DNAM) == 'T-ALL'
    assert Subtype.group('DUX4-r', GEX) == 'DUX4-r'
    assert Subtype.group('DUX4-r', DNAM) == 'DUX4-r'
    assert Subtype.group('PAX5alt', GEX) == 'PAX5alt'
    assert Subtype.group('PAX5alt', DNAM) == 'PAX5alt'
    assert Subtype.group('KMT2A-r', GEX) == 'KMT2A-r'
    assert Subtype.group('KMT2A-r', DNAM) == 'KMT2A-r'
    assert Subtype.group('ZNF384-r', GEX) == 'ZNF384-r'
    assert Subtype.group('ZNF384-r', DNAM) == 'ZNF384-r'
    assert Subtype.group('TCF3::PBX1', GEX) == 'TCF3::PBX1'
    assert Subtype.group('TCF3::PBX1', DNAM) == 'TCF3::PBX1'
    assert Subtype.group('MEF2D-r', GEX) == 'MEF2D-r'
    assert Subtype.group('MEF2D-r', DNAM) == 'MEF2D-r'
    assert Subtype.group('PAX5 P80R', GEX) == 'PAX5 P80R'
    assert Subtype.group('PAX5 P80R', DNAM) == 'PAX5 P80R'
    assert Subtype.group('NUTM1-r', GEX) == 'NUTM1-r'


def test_groups():
    assert Subtype.groups(GEX) == ['aneuploidy', 'ph-group', 'ETV6-group', 'T-ALL', 'DUX4-r', 'PAX5alt', 'KMT2A-r', 'ZNF384-r', 'TCF3::PBX1', 'MEF2D-r', 'PAX5 P80R', 'NUTM1-r', 'Control']
    assert Subtype.groups(DNAM) == ['aneuploidy', 'ph-group', 'ETV6-group', 'T-ALL', 'DUX4-r', 'PAX5alt', 'KMT2A-r', 'ZNF384-r', 'TCF3::PBX1', 'MEF2D-r', 'PAX5 P80R', 'NUTM1-r', 'Control']


def test_subtypes():
    assert Subtype.subtypes(GEX) == ['high hyperdiploid', 'low hyperdiploid', 'iAMP21', 'BCR::ABL1', 'BCR::ABL1-like', 'ETV6::RUNX1', 'ETV6::RUNX1-like', 'T-ALL', 'DUX4-r', 'PAX5alt', 'KMT2A-r', 'ZNF384-r', 'TCF3::PBX1', 'MEF2D-r', 'PAX5 P80R', 'NUTM1-r', 'Control']
    assert Subtype.subtypes(DNAM) == ['high hyperdiploid', 'low hyperdiploid', 'iAMP21', 'hypodiploid', 'BCR::ABL1', 'BCR::ABL1-like', 'ETV6::RUNX1', 'ETV6::RUNX1-like', 'T-ALL', 'DUX4-r', 'PAX5alt', 'KMT2A-r', 'ZNF384-r', 'TCF3::PBX1', 'MEF2D-r', 'PAX5 P80R', 'NUTM1-r', 'Control']
