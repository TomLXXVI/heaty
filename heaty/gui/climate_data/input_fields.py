from heaty.gui.settings.settings import Units
from heaty.gui.user_input import processing


def get_fields():
    return {
        'T_e_d': {
            'label': 'T_e_d',
            'tooltip': 'external design temperature',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.temperature),
            'valid_range': processing.OpenInterval((float('-inf'), float('inf')), 'degC')
        },
        'T_e_an': {
            'label': 'T_e_an',
            'tooltip': 'annual mean external temperature',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.temperature),
            'valid_range': processing.OpenInterval((float('-inf'), float('inf')), 'degC')
        },
        'T_e_min': {
            'label': 'T_e_min',
            'tooltip': 'average minimum external temperature of the coldest month',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.temperature),
            'valid_range': processing.OpenInterval((float('-inf'), float('inf')), 'degC')
        }
    }
