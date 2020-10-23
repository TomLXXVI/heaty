from typing import Dict, Union, Any
from heaty.quantity.scalar import Quantity as Qty


class UnPacker:

    def __init__(self, params: Dict[str, Union[str, int, float, Qty]]):
        self.params = params

    def unpack(self, param: str, unit: str = '', default_value: Any = 0.0) -> Union[str, int, float, None]:
        val = self.params.pop(param, default_value)
        if isinstance(val, Qty):
            return val(unit)
        elif not val:
            return None
        else:
            return val
