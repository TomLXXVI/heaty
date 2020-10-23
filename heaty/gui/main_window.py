import webbrowser

from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
from heaty.gui.about import AboutDialog
from heaty.gui.climate_data.dialog import ClimateDataDialog
from heaty.gui.controller import Controller
from heaty.gui.heated_space.dialog import HeatedSpaceDialog
from heaty.gui.settings import settings
from heaty.gui.settings.dialog import SettingsDialog
from heaty.gui.settings.settings import Paths
from heaty.gui.ventilation_zone.dialog import VentilationZoneDialog


# noinspection PyArgumentList
class BuildingForm(qtw.QWidget):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        layout = qtw.QVBoxLayout()
        self.setLayout(layout)

        gpb = qtw.QGroupBox('Building', self)
        gpb_layout = qtw.QVBoxLayout()
        gpb.setLayout(gpb_layout)

        lbl_name = qtw.QLabel('Edit name')
        self.led_name = qtw.QLineEdit()
        self.led_name.setText(self.controller.building.name)
        self.led_name.returnPressed.connect(self._edit_name)
        lbl_add_be = qtw.QLabel('Add building entity')
        self.led_be_name = qtw.QLineEdit()
        self.led_be_name.setPlaceholderText('Enter a name and hit <Enter>-key')
        self.led_be_name.returnPressed.connect(self._add_building_entity)
        btn_delete = qtw.QPushButton('Delete Building', clicked=self._delete_building)

        gpb_layout.addWidget(lbl_name)
        gpb_layout.addWidget(self.led_name)
        gpb_layout.addWidget(lbl_add_be)
        gpb_layout.addWidget(self.led_be_name)
        gpb_layout.addWidget(btn_delete)

        layout.addWidget(gpb)
        layout.addStretch()

    def _edit_name(self):
        self.controller.edit_name(self.led_name.text())

    def _add_building_entity(self):
        be_name = self.led_be_name.text()
        if be_name:
            self.controller.add_building_entity(be_name)
            self.controller.update_tree()

    def _delete_building(self):
        response = qtw.QMessageBox.question(
            self,
            'Delete Building',
            'This will action will remove all the contents of the building. Are you sure?'
        )
        if response == qtw.QMessageBox.Yes:
            self.controller.delete_current_selection()
            self.controller.update_tree()

    def clear(self):
        self.led_name.setText('')
        self.led_be_name.setText('')


# noinspection PyArgumentList
class BuildingEntityForm(qtw.QWidget):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        layout = qtw.QVBoxLayout()
        self.setLayout(layout)

        gpb = qtw.QGroupBox('Building Entity')
        gpb_layout = qtw.QVBoxLayout()
        gpb.setLayout(gpb_layout)

        lbl_name = qtw.QLabel('Edit name')
        self.led_name = qtw.QLineEdit()
        self.led_name.returnPressed.connect(self._edit_name)
        lbl_add_vz = qtw.QLabel('Add ventilation zone')
        self.led_vz_name = qtw.QLineEdit()
        self.led_vz_name.setPlaceholderText('Enter a name and hit <Enter>-key')
        self.led_vz_name.returnPressed.connect(self._add_ventilation_zone)
        btn_delete = qtw.QPushButton('Delete Building Entity', clicked=self._delete_building_entity)

        gpb_layout.addWidget(lbl_name)
        gpb_layout.addWidget(self.led_name)
        gpb_layout.addWidget(lbl_add_vz)
        gpb_layout.addWidget(self.led_vz_name)
        gpb_layout.addWidget(btn_delete)

        layout.addWidget(gpb)
        layout.addStretch()

    def _edit_name(self):
        self.controller.edit_name(self.led_name.text())

    def _add_ventilation_zone(self):
        vz_name = self.led_vz_name.text()
        if vz_name:
            vz_dlg = VentilationZoneDialog(self, vz_name=vz_name)
            if vz_dlg.exec_():
                self.controller.update_tree()
            else:
                pass

    def _delete_building_entity(self):
        response = qtw.QMessageBox.question(
            self,
            'Delete Building Entity',
            'This action will remove the building entity and all of its contents. Are you sure?'
        )
        if response == qtw.QMessageBox.Yes:
            self.controller.delete_current_selection()
            self.controller.update_tree()

    def clear(self):
        self.led_name.setText('')
        self.led_vz_name.setText('')


# noinspection PyArgumentList
class VentilationZoneForm(qtw.QWidget):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        layout = qtw.QVBoxLayout()
        self.setLayout(layout)

        gpb = qtw.QGroupBox('Ventilation Zone')
        gpb_layout = qtw.QVBoxLayout()
        gpb.setLayout(gpb_layout)

        lbl_name = qtw.QLabel('Edit name')
        self.led_name = qtw.QLineEdit()
        self.led_name.returnPressed.connect(self._edit_name)
        lbl_add_hs = qtw.QLabel('Add heated space')
        self.led_hs_name = qtw.QLineEdit()
        self.led_hs_name.setPlaceholderText('Enter a name and hit <Enter>-key')
        self.led_hs_name.returnPressed.connect(self._add_heated_space)
        btn_modify = qtw.QPushButton('Modify Ventilation Zone...', clicked=self._modify_ventilation_zone)
        btn_delete = qtw.QPushButton('Delete Ventilation Zone', clicked=self._delete_ventilation_zone)

        gpb_layout.addWidget(lbl_name)
        gpb_layout.addWidget(self.led_name)
        gpb_layout.addWidget(lbl_add_hs)
        gpb_layout.addWidget(self.led_hs_name)
        gpb_layout.addWidget(btn_modify)
        gpb_layout.addWidget(btn_delete)

        layout.addWidget(gpb)
        layout.addStretch()

    def _edit_name(self):
        self.controller.edit_name(self.led_name.text())

    def _add_heated_space(self):
        hs_name = self.led_hs_name.text()
        if hs_name:
            hs_dlg = HeatedSpaceDialog(self, name=hs_name)
            if hs_dlg.exec_():
                self.controller.update_tree()
            else:
                pass

    def _modify_ventilation_zone(self):
        vz_params = self.controller.fetch_ventilation_zone_params()
        vz_dlg = VentilationZoneDialog(self, vz_name=self.led_name.text(), params=vz_params, mode='modify')
        if vz_dlg.exec_():
            self.controller.update_tree()
        else:
            pass

    def _delete_ventilation_zone(self):
        response = qtw.QMessageBox.question(
            self,
            'Delete Ventilation Zone',
            'This action will remove the ventilation zone and all of its contents. Are you sure?'
        )
        if response == qtw.QMessageBox.Yes:
            self.controller.delete_current_selection()
            self.controller.update_tree()

    def clear(self):
        self.led_name.setText('')
        self.led_hs_name.setText('')


# noinspection PyArgumentList
class HeatedSpaceForm(qtw.QWidget):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller: Controller = controller

        layout = qtw.QVBoxLayout()
        self.setLayout(layout)

        gpb = qtw.QGroupBox('Heated Space')
        gpb_layout = qtw.QVBoxLayout()
        gpb.setLayout(gpb_layout)

        lbl_name = qtw.QLabel('Edit name')
        self.led_name = qtw.QLineEdit()
        self.led_name.returnPressed.connect(self._edit_name)
        btn_modify = qtw.QPushButton('Modify Heated Space...', clicked=self._modify_heated_space)
        btn_delete = qtw.QPushButton('Delete Heated Space', clicked=self._delete_heated_space)

        gpb_layout.addWidget(lbl_name)
        gpb_layout.addWidget(self.led_name)
        gpb_layout.addWidget(btn_modify)
        gpb_layout.addWidget(btn_delete)

        layout.addWidget(gpb)
        layout.addStretch()

    def _edit_name(self):
        self.controller.edit_name(self.led_name.text())

    def _modify_heated_space(self):
        hs_params = self.controller.fetch_heated_space_params()
        bem_data = self.controller.fetch_building_element_data()
        hs_dlg = HeatedSpaceDialog(
            self,
            name=self.led_name.text(),
            params=hs_params,
            bem_items=bem_data,
            mode='modify'
        )
        if hs_dlg.exec_():
            self.controller.update_tree()
        else:
            pass

    def _delete_heated_space(self):
        response = qtw.QMessageBox.question(
            self,
            'Delete Heated Spaces',
            'This action will remove the heated space. Are you sure?'
        )
        if response == qtw.QMessageBox.Yes:
            self.controller.delete_current_selection()
            self.controller.update_tree()

    def clear(self):
        self.led_name.setText('')


class StackedWidget(qtw.QStackedWidget):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # connect internal methods to the controller slots
        self.controller.connect_to_slot('display', self.display)
        self.controller.connect_to_slot('clear', self.clear)

        # keep a list of the page indexes that are in the stacked widget
        self._form_indices = [
            self.addWidget(BuildingForm(self, controller)),
            self.addWidget(BuildingEntityForm(self, controller)),
            self.addWidget(VentilationZoneForm(self, controller)),
            self.addWidget(HeatedSpaceForm(self, controller))
        ]

    def display(self, **kwargs):
        # this method is connected to the display slot of the controller
        self.setCurrentIndex(kwargs['level'])
        widget = self.currentWidget()
        widget.led_name.setText(kwargs['name'])

    def clear(self):
        # this method is connected to the clear slot of the controller
        for i in self._form_indices:
            self.setCurrentIndex(i)
            form = self.currentWidget()
            form.clear()
        self.setCurrentIndex(0)


# noinspection PyUnresolvedReferences,PyArgumentList
class MainWidget(qtw.QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.controller: Controller = parent.controller

        main_layout = qtw.QVBoxLayout()
        self.setLayout(main_layout)

        body_layout = qtw.QHBoxLayout()
        main_layout.addLayout(body_layout)

        left_layout = qtw.QVBoxLayout()
        body_layout.addLayout(left_layout)

        frame = qtw.QFrame(self)
        frame.setLayout(qtw.QVBoxLayout())

        gpb_climate = qtw.QGroupBox('Climate Data')
        gpb_climate.setLayout(qtw.QVBoxLayout())

        lbl_Ted = qtw.QLabel('External Design Temperature', self)
        self.led_Ted = qtw.QLabel(self)
        params = self.controller.get_climate_data_params()
        self.led_Ted.setText(f"<h1>{params['T_e_d'].value:.1f} {params['T_e_d'].unit}</h1>")
        btn_climate = qtw.QPushButton('Set Climate Data...', clicked=self.set_climate_data)

        gpb_climate.layout().addWidget(lbl_Ted)
        gpb_climate.layout().addWidget(self.led_Ted, 0, qtc.Qt.AlignHCenter)
        gpb_climate.layout().addWidget(btn_climate)

        frame.layout().addWidget(gpb_climate)

        left_layout.addWidget(frame)

        self.stacked_widget = StackedWidget(self, self.controller)
        left_layout.addWidget(self.stacked_widget)

        self.tree_view = qtw.QTreeView(self)
        self.controller.init_tree(self.tree_view)

        body_layout.addWidget(self.tree_view)
        body_layout.setStretchFactor(left_layout, 1)
        body_layout.setStretchFactor(self.tree_view, 4)

    def set_climate_data(self):
        params = self.controller.get_climate_data_params()
        clima_dlg = ClimateDataDialog(parent=self, params=params)
        if clima_dlg.exec_():
            params = self.controller.get_climate_data_params()
            self.led_Ted.setText(f"<h1>{params['T_e_d'].value:.1f} {params['T_e_d'].unit}</h1>")
        else:
            pass


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Heaty')
        ICON_PATH = settings.find_file(settings.RESOURCES_PATH, 'house.ico')
        self.setWindowIcon(qtg.QIcon(ICON_PATH))
        size = qtw.QDesktopWidget().availableGeometry(self).size()
        self.resize(0.7 * size)

        self.controller = Controller()
        settings.load_program_settings()

        self._create_menubar()

        main_widget = MainWidget(self)

        self.statusbar = self.statusBar()

        self.setCentralWidget(main_widget)

        self.show()

    def _create_menubar(self):
        menubar = self.menuBar()

        project_menu = menubar.addMenu('&Project')

        project_new = project_menu.addAction('New')
        project_new.setStatusTip('Create new file')
        project_new.triggered.connect(self._new)

        project_open = project_menu.addAction('Open...')
        project_open.setStatusTip('Open existing file from disk')
        project_open.triggered.connect(self._open)

        project_menu.addSeparator()

        project_save = project_menu.addAction('Save...')
        project_save.setStatusTip('Save file to disk')
        project_save.triggered.connect(self._save)

        project_export = project_menu.addAction('Export...')
        project_export.setStatusTip('Export file as CSV')
        project_export.triggered.connect(self._export)

        project_menu.addSeparator()

        project_pref = project_menu.addAction('Preferences...')
        project_pref.setStatusTip('Change global project settings')
        project_pref.triggered.connect(self._preferences)

        project_menu.addSeparator()

        project_exit = project_menu.addAction('Exit')
        project_exit.setStatusTip('Terminate the program')
        project_exit.triggered.connect(self._exit)

        help_menu = menubar.addMenu('&Help')

        help_guide = help_menu.addAction('User Guide...')
        help_guide.setStatusTip('Open the user guide')
        help_guide.triggered.connect(self._open_user_guide)
        help_menu.addSeparator()
        help_about = help_menu.addAction('About...')
        help_about.setStatusTip('Short info about the program and its license')
        help_about.triggered.connect(self._about)

    def _new(self):
        response = qtw.QMessageBox.question(
            self,
            'New file...',
            'This action will end the current session without saving. Continue?'
        )
        if response == qtw.QMessageBox.Yes:
            self.controller.clear()
            self.controller.update_tree()

    def _exit(self):
        response = qtw.QMessageBox.question(
            self,
            'Exit program...',
            'This action will terminate the program without saving. Continue?'
        )
        if response == qtw.QMessageBox.Yes:
            self.close()

    def _save(self):
        filename, _ = qtw.QFileDialog.getSaveFileName(
            self,
            "Select the file to save to...",
            Paths.paths['PROJECT_PATH'],
            'Project Files (*.hlc)',
            'Project Files (*.hlc)',
            qtw.QFileDialog.DontUseNativeDialog |
            qtw.QFileDialog.DontResolveSymlinks
        )
        if filename:
            try:
                self.controller.save(filename)
            except (ValueError, FileExistsError) as err:
                qtw.QMessageBox.critical(self, 'File Error', f'Could not save file: {err}')

    def _open(self):
        response = qtw.QMessageBox.question(
            self,
            'New file...',
            'This action will end the current session without saving. Continue?'
        )
        if response == qtw.QMessageBox.Yes:
            filename, _ = qtw.QFileDialog.getOpenFileName(
                self,
                "Select project file to open...",
                Paths.paths['PROJECT_PATH'],
                'Project Files (*.hlc)',
                'Project Files (*.hlc)',
                qtw.QFileDialog.DontUseNativeDialog |
                qtw.QFileDialog.DontResolveSymlinks
            )
            if filename:
                try:
                    self.controller.load(filename)
                except (ValueError, FileNotFoundError) as err:
                    qtw.QMessageBox.critical(self, 'File Error', f'Could not load file: {err}')
                else:
                    self.controller.update_tree()

    def _export(self):
        filename, _ = qtw.QFileDialog.getSaveFileName(
            self,
            "Select the file to export to...",
            Paths.paths['EXPORT_PATH'],
            'CSV Files (*.csv)',
            'CSV Files (*.csv)',
            qtw.QFileDialog.DontUseNativeDialog |
            qtw.QFileDialog.DontResolveSymlinks
        )
        if filename:
            try:
                self.controller.to_csv(filename)
            except (ValueError, FileExistsError) as err:
                qtw.QMessageBox.critical(self, 'File Error', f'Could not save file: {err}')

    def _preferences(self):
        settings_dlg = SettingsDialog(self)
        if settings_dlg.exec_():
            pass
        else:
            pass

    def _about(self):
        eula_dlg = AboutDialog(self)
        if eula_dlg.exec_():
            pass
        else:
            pass

    @staticmethod
    def _open_user_guide():
        GUIDE_PATH = settings.find_file(settings.RESOURCES_PATH, 'user_guide.pdf')
        webbrowser.open(GUIDE_PATH)
