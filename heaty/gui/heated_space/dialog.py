from typing import Optional, Dict, List

from PyQt5 import QtWidgets as qtw
from heaty.gui.auxiliary.types import ValueType
from heaty.gui.controller import Controller
from heaty.gui.heated_space.building_elements.widget import BuildingElementWidget
from heaty.gui.heated_space.input_fields import get_fields
from heaty.gui.user_input.form import InputForm, ButtonBox


# noinspection PyArgumentList,PyUnresolvedReferences
class HeatedSpaceDialog(qtw.QDialog):

    def __init__(self, parent, name: str = '', params: Optional[Dict[str, ValueType]] = None,
                 bem_items: Optional[List[Dict[str, ValueType]]] = None, mode: str = 'add'):
        super().__init__(parent, modal=True)
        self.controller: Controller = parent.controller
        self.mode = mode

        if self.mode == 'add':
            self.setWindowTitle('Add Heated Space')
            self.hs_name = name

        if self.mode == 'modify':
            self.setWindowTitle('Modify Heated Space')

        main_layout = qtw.QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setSizeConstraint(qtw.QLayout.SetFixedSize)

        body_layout = qtw.QHBoxLayout()

        left_layout = qtw.QVBoxLayout()

        self.input_form = InputForm(self, get_fields()) if params is None else InputForm(self, get_fields(), params)

        left_layout.addWidget(self.input_form)
        # left_layout.addStretch()

        right_layout = qtw.QVBoxLayout()

        gpb_building_elements = qtw.QGroupBox('Building elements')
        gpb_building_elements.setLayout(qtw.QVBoxLayout())
        self.bem_widget = BuildingElementWidget(gpb_building_elements, bem_items)
        gpb_building_elements.layout().addWidget(self.bem_widget)

        right_layout.addWidget(gpb_building_elements)

        body_layout.addLayout(left_layout)
        body_layout.addLayout(right_layout)
        main_layout.addLayout(body_layout)

        buttonbox = ButtonBox(self, labels=['Submit', 'Discard'], slots=[self.accept, self.reject])
        buttonbox.buttons['Discard'].setDefault(True)

        main_layout.addWidget(buttonbox)
        self.show()

    def accept(self):
        hs_params = self.input_form.read()
        bem_items = self.bem_widget.get_bem_records()
        if self.mode == 'add':
            self.controller.add_heated_space(self.hs_name, hs_params, bem_items)
        if self.mode == 'modify':
            self.controller.modify_heated_space(hs_params, bem_items)
        super().accept()
