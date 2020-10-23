from typing import Union, List
from heaty.quantity import _PintQty, unit_registry
import pint.errors as errors


class Quantity(_PintQty):

    def __new__(
            cls,
            value: Union[float, int, str],
            unit: str
    ):
        value = cls._validate_value(value)
        return super().__new__(cls, value, unit)

    @classmethod
    def _validate_value(
            cls,
            value: Union[float, int, str]
    ) -> float:
        try:
            value = float(value)
        except ValueError:
            raise ValueError(f"value {value} is not numeric")
        else:
            return value

    def __repr__(self):
        return f"{self.__class__}({self.magnitude} [{self.units:~}])"

    def __str__(self):
        return f"{self.magnitude} [{self.units:~}]"

    def __call__(
            self,
            unit: str = '',
            fmt_spec: str = 'g',
            precision: int = 6,
            show_unit: bool = False
    ) -> Union[float, str]:
        if unit:
            # convert unit string to pint Unit object
            unit = unit_registry.parse_expression(unit)
            # convert quantity `self` to pint Quantity `qty` expressed in `unit`
            qty = self.to(unit)
        else:
            # if no unit is passed, fall back to the base units of the quantity `self`
            qty = self.to_base_units()
        if not show_unit:
            # format qty as a string and convert this string to float
            return float(f"{qty.magnitude:.{precision}{fmt_spec}}")
        else:
            # format qty as string and return this string
            return f"{qty.magnitude:.{precision}{fmt_spec}} [{qty.units:~}]"

    @property
    def value(self) -> float:
        """Get value of quantity as float."""
        return self.magnitude

    @property
    def unit(self) -> str:
        """Get unit of quantity as string."""
        return f'{self.units:~}'

    def check_unit(self, unit: str) -> bool:
        """Check if `unit` is valid for quantity `self`"""
        try:
            unit = unit_registry.parse_expression(unit)
            self.to(unit)
        except (errors.DimensionalityError, errors.UndefinedUnitError):
            return False
        else:
            return True


def convert(values: Union[float, List[float]], src_unit: str, des_unit: str) -> Union[float, List[float]]:
    """
    Convert a float value or list of float values expressed in units of `src_unit` (source unit) in a float value or
    list of float values expressed in units of `des_unit` (destination unit).
    """
    if isinstance(values, float):
        qty = _PintQty(values, unit_registry(src_unit))
        qty = qty.to(des_unit)
        return qty.magnitude
    else:
        new_values = []
        for i in range(len(values)):
            qty = _PintQty(values[i], unit_registry(src_unit))
            qty = qty.to(des_unit)
            new_values.append(qty.magnitude)
        return new_values
