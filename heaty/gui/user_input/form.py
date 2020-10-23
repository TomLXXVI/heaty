from typing import List, Tuple, Union, Callable, Optional, Dict, Any

from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
from heaty.gui.auxiliary.types import ValueType
from heaty.gui.user_input.processing import InputProcessor, Interval
from heaty.quantity.scalar import Quantity


# noinspection PyArgumentList
class InputField:

    def __init__(self, parent, name: str, tooltip: str, value: ValueType, default_unit: str, valid_interval: Interval,
                 exceptions: List[Any] = None):
        self.parent = parent
        self.name = name
        self.tooltip = tooltip
        self.value = value
        self.default_unit = default_unit
        self.processor = InputProcessor(valid_interval, exceptions)
        self._create_widgets()

    def _create_widgets(self):
        self.w_label = qtw.QLabel(self.name, self.parent, toolTip=self.tooltip)
        value, unit = self.processor.process_write(self.value)
        self.w_value = qtw.QLineEdit(value, self.parent)
        self.w_value.editingFinished.connect(lambda: self._validate(parent=self.w_value))
        if unit:
            self.w_unit = qtw.QLineEdit(unit, self.parent)
            self.w_unit.setFocusPolicy(qtc.Qt.ClickFocus)
            self.w_unit.editingFinished.connect(lambda: self._validate(parent=self.w_value))
        elif self.default_unit:
            self.w_unit = qtw.QLineEdit(self.default_unit, self.parent)
            self.w_unit.setFocusPolicy(qtc.Qt.ClickFocus)
            self.w_unit.editingFinished.connect(lambda: self._validate(parent=self.w_value))
        else:
            self.w_unit = qtw.QLineEdit('')
            self.w_unit.setDisabled(True)

    @property
    def widgets(self) -> Tuple[qtw.QLabel, qtw.QLineEdit, qtw.QLineEdit]:
        # this is method is called by the input form to layout the widgets on the form
        return self.w_label, self.w_value, self.w_unit

    def _validate(self, parent):
        value = self.w_value.text()
        unit = self.w_unit.text()
        self.processor.validate(value, unit, parent)

    def read(self) -> Tuple[str, Union[float, Quantity]]:
        label = self.w_label.text()
        value = self.w_value.text()
        unit = self.w_unit.text()
        value = self.processor.process_read(value, unit)
        return label, value

    def write(self, value: Union[float, Quantity]):
        value, unit = self.processor.process_write(value)
        self.w_value.setText(value)
        if unit: self.w_unit.setText(unit)


class InputForm(qtw.QGroupBox):

    def __init__(self, parent, fields: Union[list, dict], values: Optional[Dict[str, ValueType]] = None):
        super().__init__('Input parameters', parent)

        grid = qtw.QGridLayout()
        grid.setVerticalSpacing(10)

        self._field_widgets: Dict[str, InputField] = {}
        row_index = 0

        if isinstance(fields, dict): fields = fields.values()
        for field in fields:
            field_widget = InputField(
                parent=self,
                name=field['label'],
                tooltip=field['tooltip'],
                value=field['default_value'] if values is None else values[field['label']],
                default_unit=field['default_unit'],
                valid_interval=field['valid_range'],
                exceptions=field.get('exceptions')
            )
            self._field_widgets[field_widget.name] = field_widget
            w1, w2, w3 = field_widget.widgets
            grid.addWidget(w1, row_index, 0)
            grid.addWidget(w2, row_index, 1)
            grid.addWidget(w3, row_index, 2)
            row_index += 1

        self.setLayout(qtw.QVBoxLayout())
        self.layout().addLayout(grid)
        self.layout().addStretch()

    def read(self) -> Dict[str, ValueType]:
        # read fields of the input form and return their values in a dict {field_name: field_value, ...}
        input_values = {}
        for field_widget in self._field_widgets.values():
            label, value = field_widget.read()
            input_values[label] = value
        return input_values

    def write(self, values: Dict[str, ValueType]):
        # write to the fields of the input form; input is a dict of the form {field_name: field_value, ...}
        for name, value in values.items():
            try:
                field_widget = self._field_widgets[name]
            except KeyError:
                continue
            else:
                field_widget.write(value)


class ButtonBox(qtw.QWidget):

    def __init__(self, parent, labels: List[str], slots: Optional[List[Optional[Callable]]] = None):
        super().__init__(parent)
        self.setLayout(qtw.QHBoxLayout())
        self.buttons = {}

        for i, label in enumerate(labels):
            slot = slots[i] if slots else None
            button = qtw.QPushButton(label)
            if slot:
                button.clicked.connect(slot)
            self.layout().addWidget(button)
            self.buttons[label] = button
        self.layout().addStretch()
