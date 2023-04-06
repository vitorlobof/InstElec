from pathlib import Path
import os
from pint import UnitRegistry

BASE_DIR = Path().parent.parent.resolve()

# Units manager
ureg = UnitRegistry()
ureg.define('volt_ampere_reactive = watt = var')

# Fase-fase and neuter-fase voltages.
VOLTAGE_FF = 380*ureg.volt
VOLTAGE_FN = 220*ureg.volt

# Static files, like tables.
STATIC_DIR = os.path.join(BASE_DIR, 'static')
