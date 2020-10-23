from heaty.gui.settings.settings import Units
from heaty.gui.user_input import processing


def get_fields():
    return {
        'T_i_d': {
            'label': 'T_i_d',
            'tooltip': 'internal design temperature [EN 12831-1/B.4.2]',
            'default_value': '20.0',
            'default_unit': Units.default_unit(Units.temperature),
            'valid_range': processing.OpenInterval((float('-inf'), float('inf')), 'degC')
        },
        'A_fl': {
            'label': 'A_fl',
            'tooltip': 'floor area',
            'default_value': '1.0',
            'default_unit': Units.default_unit(Units.area),
            'valid_range': processing.OpenInterval((0.0, float('inf')), 'm ** 2')
        },
        'V_r': {
            'label': 'V_r',
            'tooltip': 'internal room volume',
            'default_value': '2.5',
            'default_unit': Units.default_unit(Units.volume),
            'valid_range': processing.OpenInterval((0.0, float('inf')), 'm ** 3')
        },
        'h_r': {
            'label': 'h_r',
            'tooltip': 'room height',
            'default_value': '2.5',
            'default_unit': Units.default_unit(Units.length),
            'valid_range': processing.OpenInterval((0.0, float('inf')), 'm')
        },
        'h_occ': {
            'label': 'h_occ',
            'tooltip': 'height of occupied zone [EN 12831-1/B.2.6]',
            'default_value': '1.0',
            'default_unit': Units.default_unit(Units.length),
            'valid_range': processing.OpenInterval((0.0, float('inf')), 'm')
        },
        'gT_a': {
            'label': 'gT_a',
            'tooltip': 'air temperature gradient [EN 12831-1/B.2.6]',
            'default_value': '1.0',
            'default_unit': Units.default_unit(Units.temperature_gradient),
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')), 'K / m')
        },
        'dT_s': {
            'label': 'dT_s',
            'tooltip': 'correction term to allow for differing air and surface temperatures [EN 12831-1/B.2.6]',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.temperature_difference),
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')), 'K')
        },
        'dT_rad': {
            'label': 'dT_rad',
            'tooltip': 'correction term to allow for differing air and operative temperatures [EN 12831-1/B.2.6]',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.temperature_difference),
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')), 'K')
        },
        'n_min': {
            'label': 'n_min',
            'tooltip': 'minimum air change of the room [EN 12831-1/B.2.10]',
            'default_value': '0.5',
            'default_unit': Units.default_unit(Units.air_change_rate),
            'valid_range': processing.OpenInterval((0.0, float('inf')), '1 / hr')
        },
        'V_open': {
            'label': 'V_open',
            'tooltip': 'external air volume flow through large openings in the building envelope [EN 12831-1/G]',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.volume_flow_rate),
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')), 'm ** 3 / hr')
        },
        'V_ATD_d': {
            'label': 'V_ATD_d',
            'tooltip': 'design air volume flow of the ATDs in the room [EN 12831-1/B.2.12]',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.volume_flow_rate),
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')), 'm ** 3 / hr')
        },
        'V_sup': {
            'label': 'V_sup',
            'tooltip': 'supply air volume flow into heated space',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.volume_flow_rate),
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')), 'm ** 3 / hr')
        },
        'V_trf': {
            'label': 'V_trf',
            'tooltip': 'transfer air volume flow from adjacent space into heated space',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.volume_flow_rate),
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')), 'm ** 3 / hr')
        },
        'V_exh': {
            'label': 'V_exh',
            'tooltip': 'exhaust air volume flow from the heated space',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.volume_flow_rate),
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')), 'm ** 3 / hr')
        },
        'V_comb': {
            'label': 'V_comb',
            'tooltip': 'air volume flow exhausted from heated space not included in V_exh (eg. combustion air)',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.volume_flow_rate),
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')), 'm ** 3 / hr')
        },
        'T_sup': {
            'label': 'T_sup',
            'tooltip': 'ventilation supply air temperature after heat recovery [EN 12831-1/6.3.3.7]',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.temperature),
            'valid_range': processing.OpenInterval((float('-inf'), float('inf')), 'degC')
        },
        'T_trf': {
            'label': 'T_trf',
            'tooltip': 'temperature of the transfer air into the heated space from another space',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.temperature),
            'valid_range': processing.OpenInterval((float('-inf'), float('inf')), 'degC')
        },
        'q_hu': {
            'label': 'q_hu',
            'tooltip': 'specific additional power for heating up',
            'default_value': '0.0',
            'default_unit': Units.default_unit(Units.power_flux),
            'valid_range': processing.ClosedOpenInterval((0.0, float('inf')), 'W / m ** 2')
        }
    }
