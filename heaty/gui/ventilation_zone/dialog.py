from typing import Optional, Dict

from PyQt5 import QtWidgets as qtw
from heaty.gui.controller import Controller, ValueType
from heaty.gui.user_input.form import InputForm, ButtonBox
from heaty.gui.ventilation_zone.input_fields import get_fields


# noinspection PyArgumentList
class VentilationZoneDialog(qtw.QDialog):

    def __init__(self, parent, vz_name: str = '', params: Optional[Dict[str, ValueType]] = None, mode: str = 'add'):
        super().__init__(parent, modal=True)
        self.controller: Controller = parent.controller
        self.mode = mode

        main_layout = qtw.QVBoxLayout()
        main_layout.setSizeConstraint(qtw.QLayout.SetFixedSize)

        if self.mode == 'add':
            self.setWindowTitle('Add Ventilation Zone')
            self.input_form = InputForm(self, get_fields())
            self.vz_name = vz_name

        if self.mode == 'modify':
            self.setWindowTitle('Modify Ventilation Zone')
            self.input_form = InputForm(self, get_fields(), params)

        buttonbox = ButtonBox(self, labels=['Submit', 'Discard'], slots=[self.accept, self.reject])
        buttonbox.buttons['Discard'].setDefault(True)

        main_layout.addWidget(self.input_form)
        main_layout.addWidget(buttonbox)

        self.setLayout(main_layout)
        self.show()

    def accept(self):
        vz_params = self.input_form.read()

        if self.mode == 'add':
            self.controller.add_ventilation_zone(self.vz_name, vz_params)

        if self.mode == 'modify':
            self.controller.modify_ventilation_zone(vz_params)

        super().accept()
