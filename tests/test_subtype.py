from subtype import Subtype
from modality import GEX, DNAM

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
