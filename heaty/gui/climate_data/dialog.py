from typing import TYPE_CHECKING, Optional, Dict

from PyQt5 import QtWidgets as qtw
from heaty.gui.auxiliary.types import ValueType
from heaty.gui.climate_data.input_fields import get_fields
from heaty.gui.user_input.form import InputForm, ButtonBox

if TYPE_CHECKING:
    from heaty.gui.controller import Controller


# noinspection PyArgumentList
class ClimateDataDialog(qtw.QDialog):

    def __init__(self, parent, params: Optional[Dict[str, ValueType]] = None):
        super().__init__(parent, modal=True)
        self.controller: Controller = parent.controller

        self.setWindowTitle('Set Climate Data')

        main_layout = qtw.QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setSizeConstraint(qtw.QLayout.SetFixedSize)

        self.input_form = InputForm(self, get_fields(), params)
        main_layout.addWidget(self.input_form)

        buttonbox = ButtonBox(self, labels=['Submit', 'Discard'], slots=[self.accept, self.reject])
        buttonbox.buttons['Discard'].setDefault(True)

        main_layout.addWidget(buttonbox)

        self.show()

    def accept(self):
        # collect user data
        params = self.input_form.read()

        # create climatic data
        self.controller.set_climate_data_params(params)

        # close dialog
        super().accept()
