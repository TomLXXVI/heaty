from typing import Optional, Dict, List

from PyQt5 import QtWidgets as qtw
from heaty.gui.auxiliary.types import ValueType
from heaty.gui.heated_space.building_elements.input_fields import get_fields
from heaty.gui.user_input.form import InputForm, ButtonBox


class Tab(qtw.QWidget):
    category = ''
    field_labels = []
    fields = []

    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(qtw.QVBoxLayout())
        self.setAutoFillBackground(True)

        self._set_fields()
        self.input_form = InputForm(self, self.fields)
        self.layout().addWidget(self.input_form)

        self.layout().addStretch()

    def read(self):
        return self.input_form.read()

    def write(self, params: Dict[str, ValueType]):
        self.input_form.write(params)

    def _set_fields(self):
        fields = get_fields()
        self.fields = [fields[lbl] for lbl in self.field_labels]


class Exterior(Tab):
    category = 'exterior'
    field_labels = ['A', 'U', 'dU_tb', 'f_U']


class AdjHeatedSpace(Tab):
    category = 'adjacent_heated_space'
    field_labels = ['A', 'U', 'T_adj']


class AdjBuildingEntity(Tab):
    category = 'adjacent_building_entity'
    field_labels = AdjHeatedSpace.field_labels


class AdjUnheatedSpace(Tab):
    category = 'adjacent_unheated_space'
    field_labels = ['A', 'U', 'f1', 'T_adj']


class Ground(Tab):
    category = 'ground'
    field_labels = ['A', 'U', 'f_dT_an', 'f_gw', 'A_g', 'P', 'dU_tb', 'z']


# noinspection PyArgumentList,PyUnresolvedReferences
class BuildingElementWidget(qtw.QWidget):

    def __init__(self, parent, bem_records: Optional[List[Dict[str, ValueType]]] = None):
        super().__init__(parent)
        self._bem_records = [] if bem_records is None else bem_records

        self.setLayout(qtw.QVBoxLayout())

        self.tab_widget = self._create_tab_widget(self)
        self.layout().addWidget(self.tab_widget)

        buttons = ButtonBox(self, labels=['Add', 'Delete'], slots=[self._add_record, self._delete_record])
        self.layout().addWidget(buttons)

        self.listbox = qtw.QListWidget()
        self.listbox.currentItemChanged.connect(lambda cur, prev: self._show_current_tab())
        self.layout().addWidget(self.listbox)

        if self._bem_records: self._add_records_to_listbox()

    def _create_tab_widget(self, parent):
        tab_widget = qtw.QTabWidget(parent)
        tab_widget.setUsesScrollButtons(False)

        self.tab_indices = {
            'exterior': tab_widget.addTab(
                Exterior(tab_widget),
                'Exterior'
            ),
            'adjacent_heated_space': tab_widget.addTab(
                AdjHeatedSpace(tab_widget),
                'Heated Space'
            ),
            'adjacent_unheated_space': tab_widget.addTab(
                AdjUnheatedSpace(tab_widget),
                'Unheated Space'
            ),
            'ground':
                tab_widget.addTab(
                    Ground(tab_widget),
                    'Ground'
                ),
            'adjacent_building_entity':
                tab_widget.addTab(
                    AdjBuildingEntity(tab_widget),
                    'Building Entity'
                )
        }

        return tab_widget

    def _add_record(self):
        # get currently active tab page
        current_tab: Tab = self.tab_widget.currentWidget()
        try:
            # read building element record from tab page
            bem_record = current_tab.read()
        except ValueError as err:
            qtw.QMessageBox.critical(self, 'Input Error', f'Could not accept input. Reason: {err}')
        else:
            # add building element category to record
            bem_record['category'] = current_tab.category
            # add new building element record to the building element data container
            self._bem_records.append(bem_record)
            # show building element in list box
            self._add_record_to_listbox(bem_record)

    def _add_record_to_listbox(self, bem_record):
        # create a string representation for the record
        category = bem_record['category']
        A = bem_record['A']
        U = bem_record['U']
        string = f"{category}: {A(A.unit, 'f', 3, True)}, {U(U.unit, 'f', 3, True)}"

        # add record string to listbox
        self.listbox.addItem(string)

    def _add_records_to_listbox(self):
        for record in self._bem_records:
            self._add_record_to_listbox(record)

    def _show_current_tab(self):
        # get index of currently selected record in listbox
        idx = self.listbox.currentIndex()
        try:
            # get this record from the list of records
            bem_record = self._bem_records[idx.row()]
        except IndexError:
            pass
        else:
            # show the right tab page according to the category the building element belongs to
            category = bem_record['category']
            tab_idx = self.tab_indices[category]
            self.tab_widget.setCurrentIndex(tab_idx)
            tab = self.tab_widget.currentWidget()

            # show the record in the tab page
            tab.write(bem_record)

    def _delete_record(self):
        # get index of currently selected record in listbox
        idx = self.listbox.currentIndex()
        try:
            # remove record from the list of records
            self._bem_records.pop(idx.row())
        except IndexError:
            pass
        else:
            # remove item from the list
            self.listbox.takeItem(idx.row())

    def get_bem_records(self):
        # this method is called to send the current list of records to the controller
        return self._bem_records
