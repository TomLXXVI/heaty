from typing import Dict, Union, List, Optional, Callable

import heaty.model.fileio as fileio
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from heaty.gui.auxiliary.types import ValueType
from heaty.gui.settings import settings
from heaty.model.building import HeatedSpace, VentilationZone, BuildingEntity, Building
from heaty.model.climate_data import ClimateData
from heaty.quantity.scalar import Quantity as Qty


class ClimateDataFactory:
    default_params = {
        'T_e_d':   Qty(0.0, 'degC'),
        'T_e_an':  Qty(0.0, 'degC'),
        'T_e_min': Qty(0.0, 'degC')
    }

    @classmethod
    def create(cls, params: Optional[Dict[str, ValueType]] = None) -> ClimateData:
        if params is not None:
            return ClimateData(**params)
        else:
            return ClimateData(**cls.default_params)


class BuildingFactory:
    default_name = 'building'

    @classmethod
    def create(cls, name: Optional[str] = None) -> Building:
        if name is not None:
            return Building(name)
        else:
            return Building(cls.default_name)


class BuildingEntityFactory:
    building: Building = None

    @classmethod
    def create(cls, name: str):
        # check if a building entity with the same name already exists in the building
        be = cls.building.building_entities.get(name)
        if be is None:
            # if not, create a new building entity and add it to the building
            be = BuildingEntity(cls.building, name)
            cls.building.building_entities[name] = be
        else:
            # if there is already a building entity with the same name, do create a new building entity,
            # but shift the pointer to the ventilation zones of the original building entity to the new one,
            # before replacing the original one
            be_new = BuildingEntity(cls.building, name)
            be_new.ventilation_zones = be.ventilation_zones
            cls.building.building_entities[name] = be_new


class VentilationZoneFactory:
    building_entity: BuildingEntity = None

    @classmethod
    def create(cls, name: str, params: Dict[str, ValueType]):
        vz = cls.building_entity.ventilation_zones.get(name)
        if vz is None:
            vz = VentilationZone(cls.building_entity, name, **params)  # create
            cls.building_entity.ventilation_zones[name] = vz  # add to building entity
        else:
            vz_new = VentilationZone(cls.building_entity, name, **params)  # create new
            vz_new.heated_spaces = vz.heated_spaces  # add the heated spaces of the original one to the new one
            cls.building_entity.ventilation_zones[name] = vz_new  # replace the original one with the new one


class HeatedSpaceFactory:
    ventilation_zone: VentilationZone = None
    climate_data: ClimateData = None

    @classmethod
    def create(cls, name: str, params: Dict[str, ValueType], bem_records: List[Dict[str, ValueType]]):
        hs = HeatedSpace(cls.ventilation_zone, name, cls.climate_data, **params)
        for r in bem_records: hs.add_building_element(**r)
        cls.ventilation_zone.heated_spaces[name] = hs
        # as a heated space has no children, we can safely replace an existing heated space with the same name in the
        # ventilation zone with the new one


class Controller:

    def __init__(self):
        self.climate_data = ClimateDataFactory.create()
        self.building = BuildingFactory.create()
        self.cur_selection: Union[Building, BuildingEntity, VentilationZone, HeatedSpace, None] = None
        self.cur_index: Optional[qtc.QModelIndex] = None
        self.display_slot: Optional[Callable] = None
        self.clear_slot: Optional[Callable] = None
        self.tree_model = None
        self.tree_view = None

    def connect_to_slot(self, slot_id: str, callback: Callable):
        # this method is called within the gui to connect certain actions that will be triggered by the controller
        if slot_id == 'display':
            # connect the display method of the stacked widget to the controller, to show the correct page according to
            # the currently selected item in the tree view
            self.display_slot = callback
        if slot_id == 'clear':
            # connect the clear method of the stacked widget to the controller, so that when the user chooses New from
            # the File menu the user contents in all the pages are cleared
            self.clear_slot = callback

    @property
    def climate_data(self) -> ClimateData:
        return HeatedSpaceFactory.climate_data

    @climate_data.setter
    def climate_data(self, climate_data: ClimateData):
        HeatedSpaceFactory.climate_data = climate_data

    @property
    def building(self) -> Building:
        return BuildingEntityFactory.building

    @building.setter
    def building(self, building: Building):
        BuildingEntityFactory.building = building

    def init_tree(self, tree_view):
        # this method is called when the program is launched and the main widget with the tree view is created
        self._init_tree_model()
        self._init_tree_view(tree_view)

    def _init_tree_model(self):
        self.tree_model = qtg.QStandardItemModel()
        self._update_tree_header()
        root_node = self.tree_model.invisibleRootItem()
        bu_row = self._make_building_row(self.building)
        root_node.appendRow(bu_row)

    def _update_tree_header(self):
        self.tree_model.setHorizontalHeaderLabels([
            'Name',
            f'Transmission heat loss [{settings.Units.default_unit(settings.Units.power)}]',
            f'Ventilation heat loss [{settings.Units.default_unit(settings.Units.power)}]',
            f'Heating-up power [{settings.Units.default_unit(settings.Units.power)}]',
            f'Total heat load [{settings.Units.default_unit(settings.Units.power)}]'
        ])

    def _init_tree_view(self, tree_view):
        # configure tree view widget
        self.tree_view = tree_view
        self.tree_view.setModel(self.tree_model)
        self.tree_view.header().setDefaultSectionSize(180)
        # each time the left mouse button is pressed on the tree view, the current corresponding object (building,
        # ventilation zone or heated space) is selected
        self.tree_view.pressed.connect(lambda idx: self.set_current_selection())
        # set initial current selection at building level
        self.tree_view.setCurrentIndex(self.tree_model.index(0, 0))
        self.set_current_selection()

    def update_tree(self):
        # this method is called from the gui, each time the configuration of the building has been changed and needs to
        # be reflected in the tree model and view
        # to keep it simple, the tree is first completely cleared; then the building model is iterated over and
        # the objects are represented by corresponding rows in the tree, showing the results for transmission heat loss
        # ventilation heat loss, heating-up power and total heat loss (or demand)
        self.tree_model.setRowCount(0)
        root_node = self.tree_model.invisibleRootItem()
        self._update_tree_header()
        bu_row = self._make_building_row(self.building)
        root_node.appendRow(bu_row)
        for be in self.building.building_entities.values():
            be_row = self._make_building_entity_row(be)
            bu_row[0].appendRow(be_row)
            for vz in be.ventilation_zones.values():
                vz_row = self._make_vz_row(vz)
                be_row[0].appendRow(vz_row)
                for hs in vz.heated_spaces.values():
                    hs_row = self._make_heat_space_row(hs)
                    vz_row[0].appendRow(hs_row)
        self.tree_view.expandAll()

    @staticmethod
    def _make_building_row(bu: Building):
        bu_row = [
            qtg.QStandardItem(bu.name),
            qtg.QStandardItem(f"{bu.Q_trm(settings.Units.default_unit(settings.Units.power)):.3f}"),
            # transmission heat loss of building
            qtg.QStandardItem(f"{bu.Q_ven(settings.Units.default_unit(settings.Units.power)):.3f}"),
            # ventilation heat loss of building
            qtg.QStandardItem(f"{bu.Q_hu(settings.Units.default_unit(settings.Units.power)):.3f}"),
            # heating-up power for building
            qtg.QStandardItem(f"{bu.Q_load(settings.Units.default_unit(settings.Units.power)):.3f}")
            # total heat loss of building
        ]
        return bu_row

    @staticmethod
    def _make_building_entity_row(be: BuildingEntity):
        be_row = [
            qtg.QStandardItem(be.name),
            qtg.QStandardItem(f"{be.Q_trm(settings.Units.default_unit(settings.Units.power)):.3f}"),
            qtg.QStandardItem(f"{be.Q_ven(settings.Units.default_unit(settings.Units.power)):.3f}"),
            qtg.QStandardItem(f"{be.Q_hu(settings.Units.default_unit(settings.Units.power)):.3f}"),
            qtg.QStandardItem(f"{be.Q_load(settings.Units.default_unit(settings.Units.power)):.3f}")
        ]
        return be_row

    @staticmethod
    def _make_vz_row(vz: VentilationZone):
        vz_row = [
            qtg.QStandardItem(vz.name),
            qtg.QStandardItem(''),
            qtg.QStandardItem(f"{vz.Q_ven(settings.Units.default_unit(settings.Units.power)):.3f}"),
            qtg.QStandardItem(''),
            qtg.QStandardItem('')
        ]
        return vz_row

    @staticmethod
    def _make_heat_space_row(hs: HeatedSpace):
        hs_row = [
            qtg.QStandardItem(hs.name),
            qtg.QStandardItem(f"{hs.Q_trm(settings.Units.default_unit(settings.Units.power)):.3f}"),
            qtg.QStandardItem(f"{hs.Q_ven(settings.Units.default_unit(settings.Units.power)):.3f}"),
            qtg.QStandardItem(f"{hs.Q_hu(settings.Units.default_unit(settings.Units.power)):.3f}"),
            qtg.QStandardItem(f"{hs.Q_load(settings.Units.default_unit(settings.Units.power)):.3f}")
        ]
        return hs_row

    def set_current_selection(self):
        # this method is called when the user presses the left mouse button in the tree view widget; it keeps a
        # reference to currently selected index in the tree view, it looks for the corresponding object in the building
        # and sends a signal to stacked widget to show the page that corresponds with the selected object.
        selected_indexes = self.tree_view.selectedIndexes()
        # selected indexes is a list of the index of the current item plus the indices of all its ancestors
        if len(selected_indexes) > 0:
            level = 0
            index = selected_indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        else:
            level = 0
        item_index = selected_indexes[0]
        self.cur_index = item_index.siblingAtColumn(0)
        if level == 0:    # building level
            self.cur_selection = self.building
            self.display_slot(level=0, name=self.building.name)  # update page in the stacked widget
        elif level == 1:  # building entity level
            be_name_item = self.tree_model.itemFromIndex(self.cur_index)
            be_name = be_name_item.text()
            self.cur_selection = self.building.building_entities.get(be_name)
            self.display_slot(level=1, name=be_name)
        elif level == 2:  # ventilation zone level
            vz_name_item = self.tree_model.itemFromIndex(self.cur_index)
            vz_name = vz_name_item.text()
            be_name_item = vz_name_item.parent()
            be_name = be_name_item.text()
            cur_be = self.building.building_entities.get(be_name)
            self.cur_selection = cur_be.ventilation_zones.get(vz_name)
            self.display_slot(level=2, name=vz_name)
        elif level == 3:  # heated space level
            hs_name_item = self.tree_model.itemFromIndex(self.cur_index)
            hs_name = hs_name_item.text()
            vz_name_item = hs_name_item.parent()
            vz_name = vz_name_item.text()
            be_name_item = vz_name_item.parent()
            be_name = be_name_item.text()
            cur_be = self.building.building_entities.get(be_name)
            cur_vz = cur_be.ventilation_zones.get(vz_name)
            self.cur_selection = cur_vz.heated_spaces.get(hs_name)
            self.display_slot(level=3, name=hs_name)

    def set_climate_data_params(self, params: Dict[str, ValueType]):
        # this method is called when the user has submitted the climate data dialog in the gui
        self.climate_data = ClimateDataFactory.create(params)

    def get_climate_data_params(self) -> Dict[str, ValueType]:
        # this method is called each time the user opens the climate data dialog in the gui
        params = self.climate_data.get_input_parameters()
        return params

    def add_building_entity(self, name: str):
        # this method is called when the user adds a new building entity to the building
        # the current selection is the building
        BuildingEntityFactory.building = self.cur_selection
        BuildingEntityFactory.create(name)

    def add_ventilation_zone(self, name: str, params: Dict[str, ValueType]):
        # this method is called when the user adds a new ventilation zone to the currently selected building entity
        # **the current selection is a building entity**; update the factory with the current building entity
        VentilationZoneFactory.building_entity = self.cur_selection
        VentilationZoneFactory.create(name, params)

    def fetch_ventilation_zone_params(self) -> Dict[str, ValueType]:
        # this method is called when the user wants to modify the currently selected ventilation zone;
        # it returns the input parameters of the currently selected ventilation zone object for displaying them in the
        # ventilation zone dialog
        vz = self.cur_selection
        params = vz.get_input_parameters()
        return params

    def modify_ventilation_zone(self, params: Dict[str, ValueType]):
        # this method is called when the user has submitted the ventilation zone dialog after modification
        # **the current selection is a ventilation zone**; update the factory with the current building entity
        VentilationZoneFactory.building_entity = self.cur_selection.building_entity
        VentilationZoneFactory.create(self.cur_selection.name, params)

    def add_heated_space(self, name: str, params: Dict[str, ValueType], bem_records: List[Dict[str, ValueType]]):
        # this method is called when the user adds a new heated space to the current ventilation zone
        # **the current selection is a ventilation zone**; update the factory with the current ventilation zone
        HeatedSpaceFactory.ventilation_zone = self.cur_selection
        HeatedSpaceFactory.create(name, params, bem_records)

    def fetch_heated_space_params(self) -> Dict[str, ValueType]:
        # this method is called when the user wants to modify the currently selected heated space;
        # it returns the input parameters of the currently selected heated space object for displaying them in the
        # heated space dialog
        hs = self.cur_selection  # current selection is a heated space
        params = hs.get_input_parameters()
        return params

    def fetch_building_element_data(self) -> List[Dict[str, ValueType]]:
        # this method is called when the user wants to modify the currently selected heated space;
        # it returns the building elements data of the currently selected heated space object for displaying them in the
        # heated space dialog
        hs = self.cur_selection  # current selection is a heated space
        bem_data = hs.get_bem_data()
        return bem_data

    def modify_heated_space(self, params, bem_records):
        # this method is called when the user has submitted the heated space dialog after modification
        # **the current selection is a heated space**; update the factory with the current ventilation zone
        HeatedSpaceFactory.ventilation_zone = self.cur_selection.ventilation_zone
        HeatedSpaceFactory.create(self.cur_selection.name, params, bem_records)

    def delete_current_selection(self):
        # this method is called when the user has pressed the delete button for the currently selected object
        # remove the currently selected object (heated space, ventilation zone or building entity) and its attached
        # children from the building; if the currently selected object is the building, then the whole building is
        # cleared
        if isinstance(self.cur_selection, HeatedSpace):
            hs = self.cur_selection
            vz = hs.ventilation_zone
            vz.heated_spaces.pop(hs.name)
        if isinstance(self.cur_selection, VentilationZone):
            vz = self.cur_selection
            be = vz.building_entity
            be.ventilation_zones.pop(vz.name)
        if isinstance(self.cur_selection, BuildingEntity):
            be = self.cur_selection
            self.building.building_entities.pop(be.name)
        if isinstance(self.cur_selection, Building):
            self.building.building_entities.clear()

    def clear(self):
        # this method is called when the user has selected New from the File menu
        # create a new, empty, default building
        self.building = BuildingFactory.create()
        # clear the pages of the stacked widget
        self.clear_slot()
        self.tree_view.setCurrentIndex(self.tree_model.index(0, 0))
        self.set_current_selection()

    def edit_name(self, name: str):
        # this method is called when the user has changed the name of the currently selected object in the gui
        if isinstance(self.cur_selection, HeatedSpace):
            vz = self.cur_selection.ventilation_zone
            hs = vz.heated_spaces.pop(self.cur_selection.name)
            hs.name = name
            vz.heated_spaces[hs.name] = hs
        if isinstance(self.cur_selection, VentilationZone):
            be = self.cur_selection.building_entity  # get building entity the ventilation zone belongs to
            vz = be.ventilation_zones.pop(self.cur_selection.name)  # remove ventilation zone from `be`'s dict
            vz.name = name  # rename ventilation zone
            be.ventilation_zones[vz.name] = vz  # add ventilation with its new name back to `be`'s dict
        if isinstance(self.cur_selection, BuildingEntity):
            be = self.building.building_entities.pop(self.cur_selection.name)
            be.name = name
            self.building.building_entities[be.name] = be
        if isinstance(self.cur_selection, Building):
            self.building.name = name
        # update tree model with modified name
        self.tree_model.setData(self.cur_index, name)

    def load(self, filename: str):
        self.building = fileio.load(filename)

    def save(self, filename: str):
        fileio.save(filename, self.building)

    def to_csv(self, filename: str):
        fileio.save(filename, self.building, '.csv')
