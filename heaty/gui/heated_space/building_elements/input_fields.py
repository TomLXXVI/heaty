from heaty.gui.settings.settings import Units
from heaty.gui.user_input import processing


def get_fields():
    return {
        'A': {
            'label': 'A',
            'tooltip': 'area of the building element',
            'default_value': '1.0',
            'default_unit': Units.default_unit(Units.area),
            'valid_range': processing.OpenInterval((0.0, float('inf')), 'm ** 2')
        },
        'U': {
            'label': 'U',
            'tooltip': 'thermal transmittance of the building element',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.transmittance),
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')), 'W / (m ** 2 * K)')
        },
        'f1': {
            'label': 'f1',
            'tooltip': 'temperature adjustment factor for heat loss to unheated spaces [EN 12831-1/B.2.4]',
            'default_value': '',
            'default_unit': '',
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf'))),
            'exceptions': ['']
        },
        'dU_tb': {
            'label': 'dU_tb',
            'tooltip': 'blanket additional thermal transmittance for thermal bridges [EN 12831-1/B.2.1]',
            'default_value': '0.1',
            'default_unit': Units.default_unit(Units.transmittance),
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')), 'W / (m ** 2 * K)')
        },
        'f_U': {
            'label': 'f_U',
            'tooltip': 'correction factor for influence of building part properties and meteorological conditions '
                       '[EN 12831-1/B.2.2]',
            'default_value': '1.0',
            'default_unit': '',
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')))
        },
        'T_adj': {
            'label': 'T_adj',
            'tooltip': 'internal design temperature of adjacent space, building entity or building',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.temperature),
            'valid_range': processing.OpenInterval((float('-inf'), float('inf')), 'degC')
        },
        'f_dT_an': {
            'label': 'f_dT_an',
            'tooltip': 'correction factor for annual variation of external temperature [EN 12831-1/B.2.3]',
            'default_value': '1.45',
            'default_unit': '',
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')))
        },
        'f_gw': {
            'label': 'f_gw',
            'tooltip': 'correction factor for influence of ground water [EN 12831-1/B.2.3]',
            'default_value': '1.0',
            'default_unit': '',
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')))
        },
        'A_g': {
            'label': 'A_g',
            'tooltip': 'area of the floor slab [EN 12831-1/E]',
            'default_value': '1.0',
            'default_unit': Units.default_unit(Units.area),
            'valid_range': processing.OpenInterval((0.0, float('inf')), 'm ** 2')
        },
        'P': {
            'label': 'P',
            'tooltip': 'exposed periphery of the floor slab [EN 12831-1/E]',
            'default_value': '4.0',
            'default_unit': Units.default_unit(Units.length),
            'valid_range': processing.OpenInterval((0.0, float('inf')), 'm')
        },
        'z': {
            'label': 'z',
            'tooltip': 'depth of top edge of floor slab below ground level',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.length),
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')), 'm')
        }
    }
