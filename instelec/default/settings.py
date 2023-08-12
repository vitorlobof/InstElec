"""
Defines the base dir, constants, the unit registry (ureg), and
the paths to the tables.
"""

from pathlib import Path
import os
from pint import UnitRegistry

BASE_DIR = Path(__file__).parent.resolve()

# Units manager
ureg = UnitRegistry()
ureg.define('volt_ampere_reactive = watt = var')

# Fase-fase and neuter-fase voltages.
VOLTAGE_FF = 380*ureg.volt
VOLTAGE_FN = 220*ureg.volt

# Static files, like tables.
TABLES_DIR = BASE_DIR / 'tables'

# Paths to condutor dimensioning tables.
CONDUTOR_DIM_DIR = TABLES_DIR / 'condutor_dimensioning'

AMPERAGE_TABLE = {
    'cupper': {
        'PVC': CONDUTOR_DIM_DIR / 'cobre_pvc.csv',
        'EPR': CONDUTOR_DIM_DIR / 'cobre_epr_ou_xlpe.csv',
        'XLPE': CONDUTOR_DIM_DIR / 'cobre_epr_ou_xlpe.csv'
    },
    'aluminum': {
        'PVC': CONDUTOR_DIM_DIR / 'aluminio_pvc.csv',
        'EPR': CONDUTOR_DIM_DIR / 'aluminio_epr_ou_xlpe.csv',
        'XLPE': CONDUTOR_DIM_DIR / 'aluminio_epr_ou_xlpe.csv'
    }
}

VOLTAGE_DROP_TABLE = CONDUTOR_DIM_DIR / 'tension_fall.csv'

TEMPERATURE_TABLE = {
    'ambiente': CONDUTOR_DIM_DIR / 'temperature_correction_ambient.csv',
    'solo': CONDUTOR_DIM_DIR / 'temperature_correction_ground.csv'
}

GROUPING_TABLE = CONDUTOR_DIM_DIR / 'agrupamento.csv'

# Classes used to handle each table.

AMPERAGE_TABLE_CLASS = 'instelec.condutor_dimensioning.tables.Amperage'
VOLTAGE_DROP_TABLE_CLASS = 'instelec.condutor_dimensioning.tables.VoltageDrop'
GROUPING_TABLE_CLASS = 'instelec.condutor_dimensioning.tables.Grouping'
TEMPERATURE_TABLE_AMBIENT_CLASS = 'instelec.condutor_dimensioning.temperature_correction.TemperatureCorrectionAmbient'
TEMPERATURE_TABLE_GROUND_CLASS = 'instelec.condutor_dimensioning.temperature_correction.TemperatureCorrectionGround'
