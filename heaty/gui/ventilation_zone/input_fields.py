from heaty.gui.settings.settings import Units
from heaty.gui.user_input import processing


def get_fields():
    return {
        'q_env_50': {
            'label': 'q_env_50',
            'tooltip': 'air permeability at 50 Pa',
            'default_value': '6.0',
            'default_unit': Units.default_unit(Units.air_permeability),
            'valid_range': processing.OpenInterval((float('-inf'), float('inf')), 'm / hr')
        },
        'V_ATD_d': {
            'label': 'V_ATD_d',
            'tooltip': 'design air volume flow of the ATDs in the zone',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.volume_flow_rate),
            'valid_range': processing.OpenInterval((float('-inf'), float('inf')), 'm ** 3 / hr')
        },
        'dP_ATD_d': {
            'label': 'dP_ATD_d',
            'tooltip': 'design pressure difference of the ATDs in the zone',
            'default_value': '4.0',
            'default_unit': Units.default_unit(Units.pressure),
            'valid_range': processing.OpenInterval((float('-inf'), float('inf')), 'Pa')
        },
        'v_leak': {
            'label': 'v_leak',
            'tooltip': 'pressure exponent of zone',
            'default_value': '0.67',
            'default_unit': '',
            'valid_range': processing.OpenInterval((float('-inf'), float('inf')))
        },
        'f_fac': {
            'label': 'f_fac',
            'tooltip': 'adjustment factor for the number of exposed facades of the zone',
            'default_value': '12',
            'default_unit': '',
            'valid_range': processing.OpenInterval((float('-inf'), float('inf')))
        },
        'f_V': {
            'label': 'f_V',
            'tooltip': 'volume flow factor of the zone',
            'default_value': '0.05',
            'default_unit': '',
            'valid_range': processing.OpenInterval((float('-inf'), float('inf')))
        },
        'f_dir': {
            'label': 'f_dir',
            'tooltip': 'factor for orientation of ventilation zone',
            'default_value': '2.0',
            'default_unit': '',
            'valid_range': processing.OpenInterval((float('-inf'), float('inf')))
        },
        'f_iz': {
            'label': 'f_iz',
            'tooltip': 'ratio between minimum air volume flow of the room and that of the entire zone',
            'default_value': '0.5',
            'default_unit': '',
            'valid_range': processing.OpenInterval((float('-inf'), float('inf')))
        },
    }
