import math
from heaty.quantity.scalar import Quantity as Qty
from heaty.model import UnPacker


def mean_internal_surface_temperature(**params) -> float:
    """
    In case of a heated space with a room height of 4 metres or higher, adjust mean internal surface temperature of a
    building element used in the calculation of temperature adjustment factors for transmission heat transfer
    coefficients, taking into account a vertical air temperature gradient and a difference between air and surface
    temperature

    **params**
    -   `T_i_d`
        Internal design temperature of the room.
    -   `gT_a`
        Air temperature gradient of the heat emission system used in the room; see EN 12831-1 B.2.6.
    -   `h`
        Mean height of the considered building element above floor level.
    -   `h_occ`
        Height of the occupied zone in the room (default 1 m cf. EN 12831-1 B.2.6).
    -   `dT_s`
        Correction term to allow for differing air and surface temperatures (e.g. increased floor or wall temperatures
        due to illumination, by radiant heaters, due to floor heating); see EN 12831-1 B.2.6.
    """
    unpacker = UnPacker(params)
    T_i_d: float = unpacker.unpack('T_i_d', 'degC')
    gT_a: float = unpacker.unpack('gT_a', 'K / m', 1.0)  # see EN 12831-1, Annex B.2.6, table B.3
    h: float = unpacker.unpack('h', 'm', 0.0)
    h_occ: float = unpacker.unpack('h_occ', 'm', 1.0)  # see EN 12831-1, Annex B.2.6
    dT_s: float = unpacker.unpack('dT_s', 'K', 0.0)  # see EN 12831-1, Annex B.2.6, table B.3
    T_sm = T_i_d + gT_a * (h - h_occ) + dT_s
    return T_sm


def mean_internal_air_temperature(**params) -> float:
    """
    Adjust internal design temperature in the calculation of ventilation heat loss to account for vertical air
    temperature gradient and for difference between operative temperature and air temperature, when room height is
    4 metres or higher.

    **params**
    -   `T_i_d`
        Internal design temperature of the room.
    -   `gT_a`
        Air temperature gradient of the heat emission system used in the room; see EN 12831-1 B.2.6.
    -   `h`
        Mean height of the considered building element above floor level.
    -   `h_occ`
        Height of the occupied zone in the room (default 1 m cf. EN 12831-1 B.2.6).
    -   `dT_rad`
        Correction term to allow for differing air and operative temperatures; see EN 12831-1 B.2.6.
    """
    unpacker = UnPacker(params)
    T_i_d: float = unpacker.unpack('T_i_d', 'degC')
    gT_a: float = unpacker.unpack('gT_a', 'K / m', 1.0)  # see EN 12831-1, Annex B.2.6, table B.3
    h: float = unpacker.unpack('h', 'm', 0.0)
    h_occ: float = unpacker.unpack('h_occ', 'm', 1.0)  # see EN 12831-1, Annex B.2.6
    dT_rad: float = unpacker.unpack('dT_rad', 'K', 0.0)  # see EN 12831-1, Annex B.2.6, table B.3
    T_ai = T_i_d + gT_a * (0.5 * h - h_occ) - dT_rad
    return T_ai


def building_time_constant(**params) -> float:
    """
    Estimate thermal time constant of building or building entity.

    **params**
    -   `c_eff`
         Volume-specific effective thermal storage capacity of the building or building entity;
    -   `V_ext`
        External / gross volume of the building or building entity.
    -   `HT`
         Overall heat transfer coefficient of the considered building without temperature adjustment.
         Only heat losses concerning the building as a whole shall be taken into account:
            + transmission heat loss (both directly or through unheated spaces):
            + to the external (directly and through unheated spaces);
            + to the ground;
            + to adjacent buildings;
            + ventilation heat loss calculated for the entire building
        Note that the conditions assumed when calculating H may differ depending on the period of time H shall be
        calculated for (e.g. different air exchange rates in daily use and weekend setback). Thus, for the same building
        and different situations, different heat transfer coefficients and accordingly different time constants may be
        calculated.
    """
    unpacker = UnPacker(params)
    c_eff: float = unpacker.unpack('c_eff', 'W * hr / (m ** 3 * K)', 50)  # see EN 12831-1, Annex B.2.7, table B.4
    V_ext: float = unpacker.unpack('V_ext', 'm ** 3')
    HT: float = unpacker.unpack('HT', 'W / K')
    C_eff = c_eff * V_ext
    tau = C_eff / HT
    return tau


def external_design_temperature(**params) -> float:
    """
    Adjust external design temperature to account for influence of geographical height and influence of thermal mass
    of the building.

    **params**
    -   `T_e_ref`
        External design temperature for the designated reference site.
    -   `gT_ref`
        Temperature gradient for the designated reference site; see NBN EN 12831-1 Annex NA.2.
    -   `h_build`
        Mean height of the considered building above sea level (or ground level at the building site).
    -   `h_ref`
        Height of reference site above sea level.
    -   `k_tau`
        Slope; see EN 12831-1 B.4.1, table B.13.
    -   `tau`
        Time constant of the considered building.
    -   `dT_e_0`
        Basic value; see EN 12831-1 B.4.1, table B.13.
    -   `dT_e_max`
        Upper limit; see EN 12831-1 B.4.1, table B.13.
    -   `dT_e_min`
        Lower limit; see EN 12831-1 B.4.1, table B.13.
    """
    unpacker = UnPacker(params)
    T_e_ref = unpacker.unpack('T_e_ref', 'degC')
    gT_ref = unpacker.unpack('gT_ref', 'K / m')  # see NBN EN 12831-1, Annex NA.2
    h_build = unpacker.unpack('h_build', 'm')
    h_ref = unpacker.unpack('h_ref', 'm')
    k_tau = unpacker.unpack('k_tau', 'K / hr', 0.016)   # see EN 12831-1, Annex B.4.1, table B.13
    tau = unpacker.unpack('tau', 'hr')
    dT_e_0 = unpacker.unpack('dT_e_0', 'K', -0.8)     # see EN 12831-1, Annex B.4.1, table B.13
    dT_e_max = unpacker.unpack('dT_e_max', 'K', 4.0)  # see EN 12831-1, Annex B.4.1, table B.13
    dT_e_min = unpacker.unpack('dT_e_max', 'K', 0.0)  # see EN 12831-1, Annex B.4.1, table B.13
    T_e_0 = T_e_ref + gT_ref * (h_build - h_ref)
    dT_e_tau = max(min(k_tau * tau + dT_e_0, dT_e_max), dT_e_min)
    T_e_d = T_e_0 + dT_e_tau
    return T_e_d


def air_permeability_50(**params) -> float:
    """
    Calculate air permeability `q_env_50` at 50 Pa from air tightness measurement.

    **params**
    -   `V_build`
        Internal building volume (air volume).
    -   `A_env_build`
        Envelope of the building.
    -   `n_50_meas`
        Measured air change rate [1/hr] at 50 Pa determined with small openings closed.
    -   `A_small_openings`
        Total area of small openings (not ATDs).
    """
    unpacker = UnPacker(params)
    V_build = unpacker.unpack('V_build', 'm ** 3')
    A_env_build = unpacker.unpack('A_env_build', 'm ** 2')
    n_50_meas = unpacker.unpack('n_50_meas', '1 / hr')
    A_small_openings = unpacker.unpack('A_small_openings', 'cm ** 2')
    n_50 = n_50_meas + 2 * A_small_openings / V_build
    q_env_50 = n_50 * V_build / A_env_build
    return q_env_50


def temperature_drop(**params) -> Qty:
    """
    Estimate temperature drop during thermostat setback.

    **params**
    -   `T_i_d`
        Internal design temperature.
    -   `T_e_sb`
        External temperature during setback period; if unknown, the external design temperature may be assumed.
    -   `t_sb`
        Setback period.
    -   `tau`
        Building time constant.
    """
    unpacker = UnPacker(params)
    T_i_d = unpacker.unpack('T_i_d', 'degC')
    T_e_sb = unpacker.unpack('T_e_sb', 'degC')
    t_sb = unpacker.unpack('t_sb', 'hr')
    tau = unpacker.unpack('tau', 'hr')
    dT_sb = (T_i_d - T_e_sb) * (1 - math.exp(-t_sb / tau))
    return Qty(dT_sb, 'K')
