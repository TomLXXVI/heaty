from typing import Dict, List, Optional, Union
from heaty.quantity.scalar import Quantity as Qty
from heaty.model import UnPacker
from heaty.model.climate_data import ClimateData
from heaty.model.building_elements import BuildingElement, CATEGORIES
import heaty.model.auxiliary as aux


class HeatedSpace:

    def __init__(self, ventilation_zone: 'VentilationZone', name: str, climate_data: ClimateData, **params):
        """
        **params**
        -   `T_i_d`
            Internal design temperature of the considered heated space; see EN 12831-1, Annex B.4.2
        -   `A_fl`
            Floor area of heated space.
        -   `V_r`
            Volume of heated space.
        -   `h_r`
            Room height of heated space.
        -   `h_occ`
            Height of the occupied zone in the room. Only required in with large ceiling heights (≥4 m);
            see EN 12831-1, Annex B.2.6
        -   `gT_a`
            Air temperature gradient of the heat emission system used in the room; see EN 12831-1, Annex B.2.6,
            table B.3.
        -   `dT_s`
            Correction term to allow for differing air and surface temperatures (e.g. increased floor or wall
            temperatures due to illumination, by radiant heaters, due to floor heating); see EN 12831-1, Annex B.2.6,
            table B.3.
        -   `dT_rad`
            Correction term to allow for differing air and operative temperatures; see EN 12831-1, Annex B.2.6,
            table B.3.
        -   `n_min`
            Minimum air change rate of the room; see EN 12831-1, Annex B.2.10, table B.7.
        -   `V_open`
            External air volume flow through large openings in the building envelope for the room. Optional:
            only required if large openings are to be considered; see EN 12831-1 Annex G.
        -   `V_ATD_d`
            Design air volume flow of the ATDs in the room. Optional: only required with ATDs; see EN 12831-1 B.2.12.
            ATD (Air Terminal Device) is a passive device allowing air flow through a building element. It does NOT
            include air out-/inlets of fan-assisted ventilation systems.
        -   `V_sup`
            Supply air volume flow of the room in case of ventilation system with supply air.
        -   `V_trf`
            Transfer air volume flow into the heated space.
        -   `V_exh`
            Exhaust air volume flow from the heated space in case of ventilation system with exhaust air.
        -   `V_comb`
            Air volume flow exhausted from the heated space that, in case of a ventilation system, has not been
            included in the exhaust air volume flow of the ventilation system – typically, but not necessarily for
            combustion air; optional: only required if there is such a technical system (e.g. open flue heaters).
        -   `T_sup`
            Temperature of the supply air volume flow into zone after passing heat recovery, but without “active”
            preheating; optional: only required in ventilation systems with exhaust and supply air; in case of actively
            preheated supply air, `T_sup` is not the actual supply air temperature but the temperature that the supply
            air would have if it had not been preheated; see EN 12831-1 §6.3.3.7
        -   `T_trf`
            Temperature of the transfer air volume flow into the heated space from another space; optional: only
            required in spaces with internal air transfer from one space to another.
        -   `q_hu`
            Specific additional power for heating up after temperature setback for the room; see EN 12831-1, Annex F.
        """
        # name of the heated space
        self.name = name
        # input parameters
        unpacker = UnPacker(params)
        self.T_i_d: float = unpacker.unpack('T_i_d', 'degC')
        self.T_e_d: float = climate_data.T_e_d
        self.T_e_an: float = climate_data.T_e_an
        self.A_fl: float = unpacker.unpack('A_fl', 'm ** 2')
        self.V_r: float = unpacker.unpack('V_r', 'm ** 3')
        self.h_r: float = unpacker.unpack('h_r', 'm', 2.7)
        self.h_occ: float = unpacker.unpack('h_occ', 'm', 1.0)       # see EN 12831-1, Annex B.2.6
        self.gT_a: float = unpacker.unpack('gT_a', 'K / m', 1.0)     # see EN 12831-1, Annex B.2.6, table B.3
        self.dT_s: float = unpacker.unpack('dT_s', 'K', 0.0)         # see EN 12831-1, Annex B.2.6, table B.3

        self.dT_rad: float = unpacker.unpack('dT_rad', 'K', 0.0)     # see EN 12831-1, Annex B.2.6, table B.3
        self.n_min: float = unpacker.unpack('n_min', '1 / hr', 0.5)  # see EN 12831-1, Annex B.2.10, table B.7
        self.V_open: float = unpacker.unpack('V_open', 'm ** 3 / hr')
        self.V_ATD_d: float = unpacker.unpack('V_ATD_d', 'm ** 3 / hr')  # see EN 12831-1, Annex B.2.12
        self.V_sup: float = unpacker.unpack('V_sup', 'm ** 3 / hr')
        self.V_trf: float = unpacker.unpack('V_trf', 'm ** 3 / hr')
        self.V_exh: float = unpacker.unpack('V_exh', 'm ** 3 / hr')
        self.V_comb: float = unpacker.unpack('V_comb', 'm ** 3 / hr')
        self.T_sup: float = unpacker.unpack('T_sup', 'degC')
        self.T_trf: float = unpacker.unpack('T_trf', 'degC')

        self.q_hu: float = unpacker.unpack('q_hu', 'W / m ** 2')   # see EN 12831-1, Annex F
        # reference to the building elements that constitute the heated space. Building elements are stored in
        # separate lists according to their category.
        self.building_elements: Dict[str, List[BuildingElement]] = {category: [] for category in CATEGORIES}
        # reference to the ventilation zone the heated space is part of
        self.ventilation_zone: Optional[VentilationZone] = ventilation_zone

    def add_building_element(self, **params):
        """
        Create a new building element for the heated space.

        **params**
        * auxiliary parameters for all kind of building elements
            -   `category`
                Kind of building element. Possible values are:
                     + 'exterior': ExteriorBuildingElement,
                     + 'adjacent_heated_space'
                     + 'adjacent_building_entity'
                     + 'adjacent_unheated_space'
                     + 'ground'
            -   `A`
                Area of the building element; can be based on internal or external dimensions depending on context.
                Where context is unknown, `A` shall refer to external dimensions. Reference to external dimensions is
                always acceptable (conservative estimate).
            -   `U`
                Thermal transmittance of the building element, determined in accordance with EN ISO 6946 for opaque
                elements or EN ISO 10077-1 for doors and windows or from information given in European Technical
                Approvals.
            -   `f1`
                Temperature adjustment for heat loss to unheated spaces; for room heights < 4 m: see EN 12831-1,
                Annex B.2.4 or Annex D.
        * extra parameters only for building elements of type `ExteriorBuildingElement`
            -   `dU_tb`
                Blanket additional thermal transmittance for thermal bridges; incorporates thermal bridges in a
                simplified manner: see EN 12831-1, Annex B.2.1.
            -   `f_U`
                Correction factor for the influence of building part properties and meteorological conditions not taken
                into account in the calculation of U-values; see EN 12831-1, Annex B.2.2.
        * extra parameters only for building elements of type `AdjacentBuildingElement`
            -   `T_adj`
                Internal design temperature of adjacent space, building entity or neighbouring building.
                    +   adjacent to heated space -> `T_adj` = internal design temperature of adjacent heated space
                    +   adjacent to unheated space or neighbouring building ->
                            `T_adj` = temperature of unheated space or building if known, or if given
                            `f1` from EN 12831-1, Annex B.2.4 or Annex D
                    +   adjacent to building entity -> `T_adj` from EN 12831-1, Annex D
        * extra parameters only for building elements of type `GroundBuildingElement`
            -   `f_dT_an`
                Correction factor taking into account the annual variation of the external temperature; see EN 12831-1,
                Annex B.2.3.
            -   `f_gw`
                Correction factor taking into account the influence of ground water; see EN 12831-1, Annex B.2.3.
            -   `T_e_an`
                Annual mean external temperature; see NBN EN 12831-1, Annex NA.2.
            -   `A_g`
                 Area of the floor slab; see EN 12831-1, Annex E.
            -   `P`
                Exposed periphery of the floor slab; see EN 12831-1, Annex E, fig. E.2
            -   `dU_tb`
                Blanket additional thermal transmittance for thermal bridges; see EN 12831-1, Annex B.2.1, table B.1.
            -   `z`
                Depth of the top edge of the floor slab below ground level; see EN 12831-1, Annex E, fig. E.1.
        """
        # create the building element
        building_element = self._create_building_element(**params)
        # store building element in the right container according to its category
        category = params.get('category')
        self.building_elements[category].append(building_element)

    def _create_building_element(self, **params):
        category = params.get('category')
        cls = CATEGORIES[category]
        return cls(self, **params)

    def update_climate_data(self, climate_data: ClimateData):
        self.T_e_d = climate_data.T_e_d
        self.T_e_an = climate_data.T_e_an

    def get_input_parameters(self) -> Dict[str, Union[float, Qty]]:
        """Return a dictionary with the current state of the input parameters"""
        return {
            'T_i_d': Qty(self.T_i_d, 'degC'),
            'T_e_d': Qty(self.T_e_d, 'degC'),
            'T_e_an': Qty(self.T_e_an, 'degC'),
            'A_fl': Qty(self.A_fl, 'm ** 2'),
            'V_r': Qty(self.V_r, 'm ** 3'),
            'h_r': Qty(self.h_r, 'm'),
            'h_occ': Qty(self.h_occ, 'm'),
            'gT_a': Qty(self.gT_a, 'K / m'),
            'dT_s': Qty(self.dT_s, 'K'),
            'dT_rad': Qty(self.dT_rad, 'K'),
            'n_min': Qty(self.n_min, '1 / hr'),
            'V_open': Qty(self.V_open, 'm ** 3 / hr'),
            'V_ATD_d': Qty(self.V_ATD_d, 'm ** 3 / hr'),
            'V_sup': Qty(self.V_sup, 'm ** 3 / hr'),
            'V_trf': Qty(self.V_trf, 'm ** 3 / hr'),
            'V_exh': Qty(self.V_exh, 'm ** 3 / hr'),
            'V_comb': Qty(self.V_comb, 'm ** 3 / hr'),
            'T_sup': Qty(self.T_sup, 'degC'),
            'T_trf': Qty(self.T_trf, 'degC'),
            'q_hu': Qty(self.q_hu, 'W / m ** 2')
        }

    def get_bem_data(self) -> List[Dict[str, Union[str, float, Qty]]]:
        """
        Return a list of dictionaries holding the input parameters of the building elements that constitute the heated
        space.
        """
        bem_data = []
        for key in self.building_elements.keys():
            bem_list = self.building_elements[key]
            for bem in bem_list:
                input_params = bem.get_input_parameters()
                input_params['category'] = key
                bem_data.append(input_params)
        return bem_data

    @property
    def HT_ie(self) -> Qty:
        """Heat transfer coefficient from the heated space directly to exterior."""
        HT_ie = sum([be.H('W / K') for be in self.building_elements['exterior']])
        return Qty(HT_ie, 'W / K')

    @property
    def HT_ia(self) -> Qty:
        """Heat transfer coefficient from the heated space to adjacent heated spaces."""
        HT_ia = sum([be.H('W / K') for be in self.building_elements['adjacent_heated_space']])
        return Qty(HT_ia, 'W / K')

    @property
    def HT_iaBE(self) -> Qty:
        """Heat transfer coefficient from the heated space to adjacent building entities."""
        HT_iaBE = sum([be.H('W / K') for be in self.building_elements['adjacent_building_entity']])
        return Qty(HT_iaBE, 'W / K')

    @property
    def HT_iae(self) -> Qty:
        """Heat transfer coefficient from the heated space to the exterior through an adjacent unheated space or a
        neighbouring building."""
        HT_iae = sum([be.H('W / K') for be in self.building_elements['adjacent_unheated_space']])
        return Qty(HT_iae, 'W / K')

    @property
    def HT_ig(self) -> Qty:
        """Heat transfer coefficient from the heated space to the ground."""
        HT_ig = sum([be.H('W / K') for be in self.building_elements['ground']])
        return Qty(HT_ig, 'W / K')

    @property
    def Q_trm(self) -> Qty:
        """Design transmission heat loss of the heated space."""
        HT = sum([
            self.HT_ie('W / K'),
            self.HT_ia('W / K'),
            self.HT_iaBE('W / K'),
            self.HT_iae('W / K'),
            self.HT_ig('W / K')
        ])
        Q_trm = HT * (self.T_i_d - self.T_e_d)
        return Qty(Q_trm, 'W')

    @property
    def T_ia(self) -> float:
        if self.h_r >= 4.0:
            return aux.mean_internal_air_temperature(
                T_id=self.T_i_d,
                gT_a=self.gT_a,
                h=self.h_r,
                h_occ=self.h_occ,
                dT_rad=self.dT_rad
            )
        else:
            return self.T_i_d

    @property
    def A_env(self) -> Qty:
        """
        Envelope of a heated space; surface area of all building elements of a heated space in contact with external air
        or unheated spaces.
        """
        A_ext = sum([be.A for be in self.building_elements['exterior']])
        A_uhs = sum([be.A for be in self.building_elements['adjacent_unheated_space']])
        A_env_ = A_ext + A_uhs
        return Qty(A_env_, 'm ** 2')

    @property
    def V_leak_ATD(self) -> float:
        try:
            return (
                    self.ventilation_zone.V_leak * (self.A_env / self.ventilation_zone.A_env) +
                    self.ventilation_zone.V_ATD * (self.V_ATD_d / self.ventilation_zone.V_ATD_d)
            )
        except ZeroDivisionError:
            return 0.0

    @property
    def V_env(self) -> float:
        try:
            vz = self.ventilation_zone
            V_env = (vz.V_inf_add / vz.V_env) * min(vz.V_env, self.V_leak_ATD * vz.f_dir)
            V_env += (vz.V_env - vz.V_inf_add) / vz.V_env * self.V_leak_ATD
            return V_env
        except ZeroDivisionError:
            return 0.0

    @property
    def V_min(self) -> float:
        return self.n_min * self.V_r

    @property
    def V_tech(self) -> float:
        return max(self.V_sup + self.V_trf, self.V_exh + self.V_comb)

    @property
    def Q_ven(self) -> Qty:
        """Ventilation loss of the heated space."""
        VT_inf = max(self.V_env + self.V_open, self.V_min - self.V_tech) * (self.T_ia - self.T_e_d)
        VT_sup = self.V_sup * (self.T_ia - self.T_sup)
        VT_trf = self.V_trf * (self.T_ia - self.T_trf)
        Q_ven = 0.34 * (VT_inf + VT_sup + VT_trf)
        return Qty(Q_ven, 'W')

    @property
    def Q_hu(self) -> Qty:
        """Optional additional heating-up power for the heated space in case of intermittent heating."""
        Q_hu = self.A_fl * self.q_hu
        return Qty(Q_hu, 'W')

    @property
    def Q_gain(self) -> Qty:
        """Optional heat gains for the heated space that occur under design external conditions."""
        return Qty(0.0, 'W')

    @property
    def Q_load(self) -> Qty:
        """Design heat load of the heated space."""
        return self.Q_trm + self.Q_ven + self.Q_hu - self.Q_gain


class VentilationZone:

    def __init__(self, building_entity: 'BuildingEntity', name: str, **params):
        """
        **params**
        -   `q_env_50`
            Air permeability (alternatively, air change rate) at a pressure difference of 50 Pa (ATDs, if any, closed);
            see EN 12831-1, Annex B.2.10.
        -   `V_ATD_d`
            Design air volume flow of the ATDs in zone. Optional: only required with ATDs; see EN 12831-1, Annex B.2.12.
        -   `dP_ATD_d`
            Design pressure difference of the ATDs in zone. Optional: only required with ATDs; see EN 12831-1,
            Annex B.2.12.
        -   `v_leak`
            Pressure exponent of zone. Optional: only required in zones with ATDs; EN 12831-1, Annex B.2.13.
        -   `f_fac`
            Adjustment factor for the number of exposed facades of the zone. Optional: only required in zones with
            unbalanced ventilation; EN 12831-1, Annex B.2.15, table B.9.
        -   `f_V`
            Volume flow factor of the zone. Optional: not required in naturally ventilated air-tight zones without ATDs;
            see EN 12831-1, Annex B.2.11, table B.8.
        -   `f_dir`
            Adjustment factor for the orientation of the zone; see EN 12831-1, Annex B.2.14
        -   `f_iz`
            Ratio between the minimum air volume flow of the room and the resulting air volume flow of the entire zone;
            see EN 12831-1, Annex B.2.9.
        """
        self.name = name
        self.building_entity: Optional[BuildingEntity] = building_entity
        self.heated_spaces: Dict[str, HeatedSpace] = {}

        # unpack input parameters
        unpacker = UnPacker(params)
        self.q_env_50: float = unpacker.unpack('q_env_50', 'm ** 3 / (m ** 2 * hr)')
        self.V_ATD_d: float = unpacker.unpack('V_ATD_d', 'm ** 3 / hr')  # EN 12831-1, Annex B.2.12
        self.dP_ATD_d: float = unpacker.unpack('dP_ATD_d', 'Pa', 4.0)  # EN 12831-1, Annex B.2.12
        self.v_leak: float = unpacker.unpack('v_leak', default_value=0.67)  # EN 12831-1, Annex B.2.13
        self.f_fac: float = unpacker.unpack('f_fac', default_value=12.0)  # EN 12831-1, Annex B.2.15, table B.9
        self.f_V: float = unpacker.unpack('f_V', default_value=0.05)  # EN 12831-1, Annex B.2.11, table B.8
        self.f_dir: float = unpacker.unpack('f_dir', default_value=2.0)  # EN 12831-1, Annex B.2.14
        self.f_iz: float = unpacker.unpack('f_iz', default_value=0.5)  # see EN 12831-1, Annex B.2.9

    @property
    def A_env(self) -> float:
        A_env_ = 0.0
        for hs in self.heated_spaces.values():
            A_env_ += hs.A_env('m ** 2')
        return A_env_

    @property
    def V_ATD_50(self) -> float:
        return self.V_ATD_d * (50 / self.dP_ATD_d) ** self.v_leak

    @property
    def V_exh(self) -> float:
        V_exh = sum([hs.V_exh for hs in self.heated_spaces.values()])
        return V_exh

    @property
    def V_comb(self) -> float:
        V_comb = sum([hs.V_comb for hs in self.heated_spaces.values()])
        return V_comb

    @property
    def V_sup(self) -> float:
        V_sup = sum([hs.V_sup for hs in self.heated_spaces.values()])
        return V_sup

    @property
    def f_e(self) -> float:
        n = self.V_exh + self.V_comb - self.V_sup
        d = self.q_env_50 * self.A_env + self.V_ATD_50
        try:
            return 1 / (1 + (self.f_fac / self.f_V) * (n / d) ** 2)
        except ZeroDivisionError:
            return 1.0

    @property
    def V_inf_add(self) -> float:
        return (self.q_env_50 * self.A_env + self.V_ATD_50) * self.f_V * self.f_e

    @property
    def V_env(self) -> float:
        return max(self.V_exh + self.V_comb - self.V_sup, 0.0) + self.V_inf_add

    @property
    def a_ATD(self) -> float:
        try:
            return self.V_ATD_50 / (self.V_ATD_50 + self.q_env_50 * self.A_env)
        except ZeroDivisionError:
            return 0.0

    @property
    def V_leak(self) -> float:
        return (1 - self.a_ATD) * self.V_env

    @property
    def V_ATD(self) -> float:
        return self.a_ATD * self.V_env

    def get_input_parameters(self) -> Dict[str, Union[float, Qty]]:
        """Return a dictionary with the current state of the input parameters."""
        return {
            'q_env_50': Qty(self.q_env_50, 'm ** 3 / (m ** 2 * hr)'),
            'V_ATD_d': Qty(self.V_ATD_d, 'm ** 3 / hr'),
            'dP_ATD_d': Qty(self.dP_ATD_d, 'Pa'),
            'v_leak': self.v_leak,
            'f_fac': self.f_fac,
            'f_V': self.f_V,
            'f_dir': self.f_dir,
            'f_iz': self.f_iz
        }

    @property
    def Q_ven(self) -> Qty:
        """Ventilation heat loss of the zone."""
        VT = 0.0
        for hs in self.heated_spaces.values():
            VT_inf = max(hs.V_leak_ATD + hs.V_open, self.f_iz * hs.V_min - hs.V_tech) * (hs.T_ia - hs.T_e_d)
            VT_sup = hs.V_sup * (hs.T_ia - hs.T_sup)
            VT_tra = hs.V_trf * (hs.T_ia - hs.T_trf)
            VT += VT_inf + VT_sup + VT_tra
        Q_ven = 0.34 * VT
        return Qty(Q_ven, 'W')


class BuildingEntity:

    def __init__(self, building: 'Building', name: str):
        self.building = building
        self.name: str = name
        self.ventilation_zones: Dict[str, VentilationZone] = {}

    @property
    def heated_spaces(self) -> List[HeatedSpace]:
        return [
            hs
            for vz in self.ventilation_zones.values()
            for hs in vz.heated_spaces.values()
        ]

    @property
    def Q_trm(self) -> Qty:
        Q_ie = 0.0; Q_iae = 0.0; Q_iaBE = 0.0; Q_ig = 0.0
        for hs in self.heated_spaces:
            Q_ie += hs.HT_ie('W / K') * (hs.T_i_d - hs.T_e_d)
            Q_iae += hs.HT_iae('W / K') * (hs.T_i_d - hs.T_e_d)
            Q_iaBE += hs.HT_iaBE('W / K') * (hs.T_i_d - hs.T_e_d)
            Q_ig += hs.HT_ig('W / K') * (hs.T_i_d - hs.T_e_d)
        Q_trm = Q_ie + Q_iae + Q_iaBE + Q_ig
        return Qty(Q_trm, 'W')

    @property
    def Q_ven(self) -> Qty:
        Q_ven = sum([vz.Q_ven('W') for vz in self.ventilation_zones.values()])
        return Qty(Q_ven, 'W')

    @property
    def Q_hu(self) -> Qty:
        Q_hu = sum([hs.Q_hu('W') for hs in self.heated_spaces])
        return Qty(Q_hu, 'W')

    @property
    def Q_gain(self) -> Qty:
        Q_gain = sum([hs.Q_gain('W') for hs in self.heated_spaces])
        return Qty(Q_gain, 'W')

    @property
    def Q_load(self) -> Qty:
        Q_load = sum([self.Q_trm('W'), self.Q_ven('W'), self.Q_hu('W')])
        Q_load -= self.Q_gain('W')
        return Qty(Q_load, 'W')


class Building:

    def __init__(self, name: str = ''):
        self.name = name
        self.building_entities: Dict[str, BuildingEntity] = {}

    @property
    def Q_trm(self) -> Qty:
        Q_ie = 0.0; Q_iae = 0.0; Q_ig = 0.0
        for be in self.building_entities.values():
            for hs in be.heated_spaces:
                Q_ie += hs.HT_ie('W / K') * (hs.T_i_d - hs.T_e_d)
                Q_iae += hs.HT_iae('W / K') * (hs.T_i_d - hs.T_e_d)
                Q_ig += hs.HT_ig('W / K') * (hs.T_i_d - hs.T_e_d)
        Q_trm = Q_ie + Q_iae + Q_ig
        return Qty(Q_trm, 'W')

    @property
    def Q_ven(self) -> Qty:
        Q_ven = sum([be.Q_ven('W') for be in self.building_entities.values()])
        return Qty(Q_ven, 'W')

    @property
    def Q_hu(self) -> Qty:
        Q_hu = sum([be.Q_hu('W') for be in self.building_entities.values()])
        return Qty(Q_hu, 'W')

    @property
    def Q_gain(self) -> Qty:
        Q_gain = sum([be.Q_gain('W') for be in self.building_entities.values()])
        return Qty(Q_gain, 'W')

    @property
    def Q_load(self) -> Qty:
        Q_load = sum([self.Q_trm('W'), self.Q_ven('W'), self.Q_hu('W')])
        Q_load -= self.Q_gain('W')
        return Qty(Q_load, 'W')
