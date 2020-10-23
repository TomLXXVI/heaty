import pint.registry

from heaty.quantity.thermal_comfort_qties import definitions as therm_comfort_defs

# get default unit registry from pint
unit_registry = pint.UnitRegistry()

# rename pint Quantity object
_PintQty = unit_registry.Quantity

# add thermal comfort units to pint's default unit registry
for d in therm_comfort_defs:
    unit_registry.define(d)
