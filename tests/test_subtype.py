from allium.subtype import Subtype
from allium.modality import GEX, DNAM


def test_list():
    legacy_dnam_subtype_groups = {'aneuploidy': ['HeH', 'low HeH', 'iAMP21', 'Hypo'], 'ph-group': ['t(9;22)', 'ph-like'],
                     'ETV6-group': ['t(12;21)', 't(12;21)-like'],  'T-ALL': ['T-ALL'], 'DUX4-r': ['DUX4-r'],
           'PAX5alt': ['PAX5alt'], '11q23/MLL': ['11q23/MLL'], 'ZNF384-r': ['ZNF384-r'], 't(1;19)': ['t(1;19)'], 
            'MEF2D-r':['MEF2D-r'], 'PAX5 p.Pro80Arg': ['PAX5 p.Pro80Arg'], 'NUTM1-r': ['NUTM1-r'], 'Control': ['Control']}
        
    legacy_gex_subtype_groups = {'aneuploidy': ['HeH', 'low HeH', 'iAMP21'], 'ph-group': ['t(9;22)', 'ph-like'],
                     'ETV6-group': ['t(12;21)', 't(12;21)-like'],  'T-ALL': ['T-ALL'], 'DUX4-r': ['DUX4-r'],
           'PAX5alt': ['PAX5alt'], '11q23/MLL': ['11q23/MLL'], 'ZNF384-r': ['ZNF384-r'], 't(1;19)': ['t(1;19)'], 
            'MEF2D-r':['MEF2D-r'], 'PAX5 p.Pro80Arg': ['PAX5 p.Pro80Arg'], 'NUTM1-r': ['NUTM1-r'], 'Control': ['Control']}
            
    assert Subtype.all(GEX) == legacy_gex_subtype_groups
    assert Subtype.all(DNAM) == legacy_dnam_subtype_groups


def test_group():
    assert Subtype.group('HeH', GEX) == 'aneuploidy'
    assert Subtype.group('HeH', DNAM) == 'aneuploidy'
    assert Subtype.group('t(9;22)', GEX) == 'ph-group'
    assert Subtype.group('t(9;22)', DNAM) == 'ph-group'
    assert Subtype.group('t(12;21)', GEX) == 'ETV6-group'
    assert Subtype.group('t(12;21)', DNAM) == 'ETV6-group'
    assert Subtype.group('T-ALL', GEX) == 'T-ALL'
    assert Subtype.group('T-ALL', DNAM) == 'T-ALL'
    assert Subtype.group('DUX4-r', GEX) == 'DUX4-r'
    assert Subtype.group('DUX4-r', DNAM) == 'DUX4-r'
    assert Subtype.group('PAX5alt', GEX) == 'PAX5alt'
    assert Subtype.group('PAX5alt', DNAM) == 'PAX5alt'
    assert Subtype.group('11q23/MLL', GEX) == '11q23/MLL'
    assert Subtype.group('11q23/MLL', DNAM) == '11q23/MLL'
    assert Subtype.group('ZNF384-r', GEX) == 'ZNF384-r'
    assert Subtype.group('ZNF384-r', DNAM) == 'ZNF384-r'
    assert Subtype.group('t(1;19)', GEX) == 't(1;19)'
    assert Subtype.group('t(1;19)', DNAM) == 't(1;19)'
    assert Subtype.group('MEF2D-r', GEX) == 'MEF2D-r'
    assert Subtype.group('MEF2D-r', DNAM) == 'MEF2D-r'
    assert Subtype.group('PAX5 p.Pro80Arg', GEX) == 'PAX5 p.Pro80Arg'
    assert Subtype.group('PAX5 p.Pro80Arg', DNAM) == 'PAX5 p.Pro80Arg'
    assert Subtype.group('NUTM1-r', GEX) == 'NUTM1-r'


def test_groups():
    assert Subtype.groups(GEX) == ['aneuploidy', 'ph-group', 'ETV6-group', 'T-ALL', 'DUX4-r', 'PAX5alt', '11q23/MLL', 'ZNF384-r', 't(1;19)', 'MEF2D-r', 'PAX5 p.Pro80Arg', 'NUTM1-r', 'Control']
    assert Subtype.groups(DNAM) == ['aneuploidy', 'ph-group', 'ETV6-group', 'T-ALL', 'DUX4-r', 'PAX5alt', '11q23/MLL', 'ZNF384-r', 't(1;19)', 'MEF2D-r', 'PAX5 p.Pro80Arg', 'NUTM1-r', 'Control']


def test_subtypes():
    assert Subtype.subtypes(GEX) == ['HeH', 'low HeH', 'iAMP21', 't(9;22)', 'ph-like', 't(12;21)', 't(12;21)-like', 'T-ALL', 'DUX4-r', 'PAX5alt', '11q23/MLL', 'ZNF384-r', 't(1;19)', 'MEF2D-r', 'PAX5 p.Pro80Arg', 'NUTM1-r', 'Control']
    assert Subtype.subtypes(DNAM) == ['HeH', 'low HeH', 'iAMP21', 'Hypo', 't(9;22)', 'ph-like', 't(12;21)', 't(12;21)-like', 'T-ALL', 'DUX4-r', 'PAX5alt', '11q23/MLL', 'ZNF384-r', 't(1;19)', 'MEF2D-r', 'PAX5 p.Pro80Arg', 'NUTM1-r', 'Control']
