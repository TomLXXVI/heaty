from typing import Dict
from heaty.quantity.scalar import Quantity as Qty
from heaty.model import UnPacker


class ClimateData:

    def __init__(self, **params):
        """
        **params**
        -   `T_e_d`
            External design temperature of the reference site; see NBN EN 12831-1 Annex NA.2, table NA.1.
        -   `T_e_an`
            Annual mean external temperature; see NBN EN 12831-1 Annex NA.2, table NA.1.
        -   `T_e_min`
            Average minimum external temperature of the coldest month; see NBN EN 12831-1 Annex NA.2, table NA.1.
        """
        unpacker = UnPacker(params)
        self.T_e_d: float = unpacker.unpack('T_e_d', 'degC')
        self.T_e_an: float = unpacker.unpack('T_e_an', 'degC')
        self.T_e_min: float = unpacker.unpack('T_e_min', 'degC')

    def get_input_parameters(self) -> Dict[str, Qty]:
        return {
            'T_e_d': Qty(self.T_e_d, 'degC'),
            'T_e_an': Qty(self.T_e_an, 'degC'),
            'T_e_min': Qty(self.T_e_min, 'degC')
        }
