from typing import List, Union
import pickle
from pathlib import Path
import csv
from heaty.model.building import Building, BuildingEntity, VentilationZone, HeatedSpace


def load(filename) -> Building:
    if filename and Path(filename).suffix == '.hlc':
        with open(filename, 'rb') as infile:
            obj = pickle.load(infile)
            if isinstance(obj, Building):
                return obj
            else:
                raise ValueError('selected file is not a valid HLC file')
    else:
        raise FileNotFoundError


def save(filename: str, building: Building, valid_suffix='.hlc'):
    if not Path(filename).suffix.lower():
        filename += valid_suffix
    if Path(filename).suffix.lower() != valid_suffix:
        raise ValueError(f'file extension "{Path(filename).suffix}" is not valid')
    # if Path(filename).exists():
    #     raise FileExistsError(f'File "{filename}" already exists')
    if valid_suffix.lower() == '.hlc':
        with open(filename, 'wb') as outfile:
            pickle.dump(building, outfile)
    elif valid_suffix.lower() == '.csv':
        ExportToCsv(building).export(filename)


class ExportToCsv:

    def __init__(self, building: Building):
        self._building = building
        self._rows: List[List[Union[str, float]]] = []

    def _create_rows(self):
        self._rows.append(self._create_header_row())
        self._rows.append(self._create_bu_row())
        for be in self._building.building_entities.values():
            self._rows.append(self._create_be_row(be))
            for vz in be.ventilation_zones.values():
                self._rows.append(self._create_vz_row(vz))
                for hs in vz.heated_spaces.values():
                    self._rows.append(self._create_hs_row(hs))

    @staticmethod
    def _create_header_row() -> List[str]:
        return [
            'name',
            'transmission heat loss',
            'ventilation heat loss',
            'heating-up power',
            'total heat loss'
        ]

    def _create_bu_row(self) -> List[Union[str, float]]:
        row = [
            self._building.name,
            self._building.Q_trm.value,
            self._building.Q_ven.value,
            self._building.Q_hu.value,
            self._building.Q_load.value
        ]
        return row

    @staticmethod
    def _create_be_row(be: BuildingEntity) -> List[Union[str, float]]:
        row = [
            be.name,
            be.Q_trm.value,
            be.Q_ven.value,
            be.Q_hu.value,
            be.Q_load.value
        ]
        return row

    @staticmethod
    def _create_vz_row(vz: VentilationZone) -> List[Union[str, float]]:
        row = [
            vz.name,
            '',
            vz.Q_ven.value,
            '',
            ''
        ]
        return row

    @staticmethod
    def _create_hs_row(hs: HeatedSpace) -> List[Union[str, float]]:
        row = [
            hs.name,
            hs.Q_trm.value,
            hs.Q_ven.value,
            hs.Q_hu.value,
            hs.Q_load.value
        ]
        return row

    def export(self, file_path: str):
        self._create_rows()
        with open(file_path, 'w', newline='') as fh:
            writer = csv.writer(fh)
            writer.writerows(self._rows)
