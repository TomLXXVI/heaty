from typing import TYPE_CHECKING, Dict, Union
from heaty.quantity.scalar import Quantity as Qty
from heaty.model import UnPacker
import heaty.model.auxiliary as aux

if TYPE_CHECKING:
    from heaty.model.building import HeatedSpace


class BuildingElement:

    def __init__(self, heated_space: 'HeatedSpace', **params):
        """
        **params**
        - `A`
        - `U`
        - `f1`
        """
        self.heated_space = heated_space
        unpacker = UnPacker(params)
        self.A: float = unpacker.unpack('A', 'm ** 2')
        self.U: float = unpacker.unpack('U', 'W / (m ** 2 * K)')
        self.T_i_d: float = self.heated_space.T_i_d
        self.T_e_d: float = self.heated_space.T_e_d
        self.T_sm: float = self._set_T_sm(
            T_id=self.T_i_d,
            gT_a=self.heated_space.gT_a,
            h=self.heated_space.h_r,
            h_occ=self.heated_space.h_occ,
            dT_s=self.heated_space.dT_s
        )
        self.f1 = unpacker.unpack('f1', default_value=None)  # see EN 12831-1, Annex B.2.4 or Annex D
        self.T_adj = None
        self.f_T = None
        self._H = None

    def _set_T_sm(self, **params) -> float:
        if self.heated_space.h_r >= 4.0:
            return aux.mean_internal_surface_temperature(**params)
        else:
            return self.T_i_d

    def _calc_temp_adjust_factor(self) -> float:
        if self.f1 is None: self.f1 = (self.T_i_d - self.T_adj) / (self.T_i_d - self.T_e_d)
        f2 = (self.T_sm - self.T_i_d) / (self.T_i_d - self.T_e_d)
        return self.f1 + f2

    def _calc_heat_transfer_coefficient(self) -> float:
        pass

    def get_input_parameters(self) -> Dict[str, Union[str, float, Qty]]:
        """Return a dictionary with the input parameters of the building element."""
        return {
            'A': Qty(self.A, 'm ** 2'),
            'U': Qty(self.U, 'W / (m ** 2 * K)'),
            'f1': self.f1
        }

    @property
    def H(self) -> Qty:
        return Qty(self._H, 'W / K')


class ExteriorBuildingElement(BuildingElement):

    def __init__(self, heated_space: 'HeatedSpace', **params):
        """
        **params**
        - `dU_tb`
        - `f_U`
        """
        super().__init__(heated_space, **params)
        unpacker = UnPacker(params)
        self.dU_tb = unpacker.unpack('dU_tb', 'W / (m ** 2 * K)', 0.1)
        self.f_U = unpacker.unpack('f_U', default_value=1.0)
        self.T_adj = self.T_e_d
        self.f_T = self._calc_temp_adjust_factor()
        self._H = self._calc_heat_transfer_coefficient()

    def _calc_heat_transfer_coefficient(self) -> float:
        return self.A * (self.U + self.dU_tb) * self.f_U * self.f_T

    def get_input_parameters(self) -> Dict[str, Union[str, float, Qty]]:
        """Return a dictionary with the input parameters of the building element."""
        input_params = super().get_input_parameters()
        input_params.update({
            'dU_tb': Qty(self.dU_tb, 'W / (m ** 2 * K)'),
            'f_U': self.f_U
        })
        return input_params


class AdjacentBuildingElement(BuildingElement):

    def __init__(self, heated_space: 'HeatedSpace', **params):
        """
        **params**
        - `T_adj`
        """
        super().__init__(heated_space, **params)
        unpacker = UnPacker(params)
        self.T_adj = unpacker.unpack('T_adj', 'degC')
        self.f_T = self._calc_temp_adjust_factor()
        self._H = self._calc_heat_transfer_coefficient()

    def _calc_heat_transfer_coefficient(self) -> float:
        return self.A * self.U * self.f_T

    def get_input_parameters(self) -> Dict[str, Union[str, float, Qty]]:
        """Return a dictionary with the input parameters of the building element."""
        input_params = super().get_input_parameters()
        input_params.update({
            'T_adj': Qty(self.T_adj, 'degC')
        })
        return input_params


class GroundBuildingElement(BuildingElement):

    def __init__(self, heated_space: 'HeatedSpace', **params):
        """
        **params**
        - `f_dT_an`
        - `f_gw`
        - `A_g`
        - `P`
        - `dU_tb`
        - `z`
        """
        super().__init__(heated_space, **params)
        unpacker = UnPacker(params)
        self.f_dT_an = unpacker.unpack('f_dT_an', default_value=1.45)  # EN 12831-1, Annex B.2.3
        self.f_gw = unpacker.unpack('f_gw', default_value=1.0)  # EN 12831-1, Annex B.2.3
        self.A_g = unpacker.unpack('A_g', 'm ** 2')
        self.P = unpacker.unpack('P', 'm')
        self.B = self._calc_B()
        self.dU_tb = unpacker.unpack('dU_tb', 'W / (m ** 2 * K)', 0.1)
        self.z = unpacker.unpack('z', 'm', 0.0)
        self.U_equiv = self._calc_U_equiv()
        self.T_adj = self.heated_space.T_e_an
        self.f_T = self._calc_temp_adjust_factor()
        self._H = self._calc_heat_transfer_coefficient()

    def _calc_heat_transfer_coefficient(self) -> float:
        return self.f_dT_an * self.A * self.U_equiv * self.f_T * self.f_gw

    def _calc_B(self) -> float:
        return self.A_g / (0.5 * self.P)

    def _set_U_equiv_params(self):
        if self.z == 0.0:
            self.a = 0.9671
            self.b = -7.455
            self.c = (10.76, 9.773, 0.0265)
            self.d = -0.0203
            self.n = (0.5532, 0.6027, -0.9296)
        if self.z > 0.0:
            self.a = 0.93328
            self.b = -2.1552
            self.c = (0.0, 1.466, 0.1006)
            self.d = -0.0692
            self.n = (0.0, 0.45325, -1.0068)

    def _calc_U_equiv(self) -> float:
        self._set_U_equiv_params()
        t_B = (self.c[0] + self.B) ** self.n[0]
        t_z = (self.c[1] + self.z) ** self.n[1]
        t_U = (self.c[2] + self.U + self.dU_tb) ** self.n[2]
        U_equiv = self.a / (self.b + t_B + t_z + t_U) + self.d
        return U_equiv

    def get_input_parameters(self) -> Dict[str, Union[str, float, Qty]]:
        """Return a dictionary with the input parameters of the building element."""
        input_params = super().get_input_parameters()
        input_params.update({
            'f_dT_an': self.f_dT_an,
            'f_gw': self.f_gw,
            'A_g': Qty(self.A_g, 'm ** 2'),
            'P': Qty(self.P, 'm'),
            'dU_tb': Qty(self.dU_tb, 'W / (m ** 2 * K)'),
            'z': Qty(self.z, 'm')
        })
        return input_params


CATEGORIES = {
    'exterior': ExteriorBuildingElement,
    'adjacent_heated_space': AdjacentBuildingElement,
    'adjacent_building_entity': AdjacentBuildingElement,
    'adjacent_unheated_space': AdjacentBuildingElement,
    'ground': GroundBuildingElement
}
