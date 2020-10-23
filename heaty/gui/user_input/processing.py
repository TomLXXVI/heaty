from typing import Union, Tuple, Optional, List, Any

from PyQt5 import QtWidgets as qtw
from heaty.quantity.scalar import Quantity as Qty


class Interval:

    def __init__(self, default_unit: str = ''):
        self.base_quantity: Optional[Qty] = Qty(1.0, default_unit) if default_unit else None

    def _make_float(self, value: Union[str, int, float], unit: str = ''):
        pass

    def _check_unit(self, unit: str) -> bool:
        if self.base_quantity is not None and self.base_quantity.check_unit(unit):
            return True
        return False

    def _check_value(self, value: Union[str, int, float], unit: str) -> bool:
        pass

    def validate(self, value: Union[str, int, float], unit: str = '') -> bool:
        if (unit and self._check_unit(unit)) or not unit:
            if not self._check_value(value, unit):
                raise ValueError(f'Value "{value}" invalid. Valid range is {str(self)}')
            else:
                return True
        elif unit and not self._check_unit(unit):
            raise ValueError(f'Invalid unit "{unit}" for value "{value}"')

    def __str__(self):
        pass


class ContinuousInterval(Interval):

    def __init__(self, limits: Tuple[Union[str, int, float], Union[str, int, float]], default_unit: str = ''):
        super().__init__(default_unit)
        lower_value = limits[0]
        upper_value = limits[1]
        if default_unit:
            self.lower_value = Qty(lower_value, default_unit)
            self.upper_value = Qty(upper_value, default_unit)
        else:
            self.lower_value = float(lower_value)
            self.upper_value = float(upper_value)

    def _make_float(self, value: Union[str, int, float], unit: str = '') -> Tuple[float, float, float]:
        if unit:
            qty = Qty(value, unit)
            value = qty()
        else:
            value = float(value)
        if isinstance(self.lower_value, Qty) and isinstance(self.upper_value, Qty):
            lower_value = self.lower_value()
            upper_value = self.upper_value()
        else:
            lower_value = self.lower_value
            upper_value = self.upper_value
        return lower_value, value, upper_value


class ClosedInterval(ContinuousInterval):

    def _check_value(self, value: Union[str, int, float], unit: str) -> bool:
        lower_value, value, upper_value = super()._make_float(value, unit)
        if lower_value <= value <= upper_value:
            return True
        return False

    def __str__(self):
        return f"[{self.lower_value}; {self.upper_value}]"


class ClosedOpenInterval(ContinuousInterval):

    def _check_value(self, value: Union[str, int, float], unit: str) -> bool:
        lower_value, value, upper_value = super()._make_float(value, unit)
        if lower_value <= value < upper_value:
            return True
        return False

    def __str__(self):
        return f"[{self.lower_value}; {self.upper_value}["


class OpenClosedInterval(ContinuousInterval):

    def _check_value(self, value: Union[str, int, float], unit: str) -> bool:
        lower_value, value, upper_value = super()._make_float(value, unit)
        if lower_value < value <= upper_value:
            return True
        return False

    def __str__(self):
        return f"]{self.lower_value}; {self.upper_value}]"


class OpenInterval(ContinuousInterval):

    def _check_value(self, value: Union[str, int, float], unit: str) -> bool:
        lower_value, value, upper_value = super()._make_float(value, unit)
        if lower_value < value < upper_value:
            return True
        return False

    def __str__(self):
        return f"]{self.lower_value}; {self.upper_value}["


class DiscreteInterval(Interval):

    def __init__(self, allowed_values: List[Union[str, int, float]], default_unit: str = ''):
        super().__init__(default_unit)
        if default_unit:
            self.allowed_values: Union[List[Qty], List[float]] = [Qty(value, default_unit) for value in allowed_values]
        else:
            self.allowed_values: Union[List[Qty], List[float]] = [float(value) for value in allowed_values]

    def _make_float(self, value: Union[str, int, float], unit: str = '') -> Tuple[List[float], float]:
        if unit:
            qty = Qty(value, unit)
            value = qty()
        else:
            value = float(value)
        if isinstance(self.allowed_values[0], Qty):
            allowed_values = [qty() for qty in self.allowed_values]
        else:
            allowed_values = self.allowed_values
        return allowed_values, value

    def _check_value(self, value: Union[str, int, float], unit: str) -> bool:
        allowed_values, value = self._make_float(value, unit)
        if value in allowed_values:
            return True
        return False

    def __str__(self):
        string = "["
        for value in self.allowed_values[:-1]:
            string += f"{value}; "
        string += f"{self.allowed_values[-1]}]"
        return string


class InputProcessor:

    def __init__(self, valid_interval: Interval, exceptions: List[Any] = None):
        self._valid_interval = valid_interval
        self._exceptions = exceptions  # allowable exceptions on the valid interval

    def validate(self, value, unit, parent):
        try:
            self._valid_interval.validate(value, unit)
        except ValueError as err:
            if value not in self._exceptions:
                qtw.QMessageBox.critical(parent, 'Input Error', f'Could not accept input. Reason: {err}')
                parent.setFocus()

    def process_read(self, value: Union[str, int, float], unit: str = '') -> Union[Qty, float, Any]:
        """
        Transform a value (float, int or str) without unit into a float and with unit into a Quantity.
        Used for reading an InputField.
        """
        if unit:
            return Qty(value, unit)
        else:
            try:
                return float(value)
            except ValueError as err:
                if value in self._exceptions:
                    return value
                else:
                    raise err

    @staticmethod
    def process_write(value_: Union[str, int, float, Qty]) -> Tuple[str, str]:
        """
        Transform a numeric value (float, int or str) or a Quantity into a value string and/or unit. If the value is
        no Quantity an empty string is used in place of unit.
        Used for writing to an InputField.
        """
        if isinstance(value_, Qty):
            value = value_.value
            unit = value_.unit
            return str(value), unit
        else:
            return str(value_), ''
