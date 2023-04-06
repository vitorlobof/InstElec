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

# Paths to tables.
AMPERAGE_TABLE = {
    'cupper': {
        'PVC': os.path.join(STATIC_DIR, 'cobre_pvc.csv'),
        'EPR': os.path.join(STATIC_DIR, 'cobre_epr_ou_xlpe.csv'),
        'XLPE': os.path.join(STATIC_DIR, 'cobre_epr_ou_xlpe.csv')
    },
    'aluminum': {
        'PVC': os.path.join(
            STATIC_DIR, 'aluminio_pvc.csv'),
        'EPR': os.path.join(
            STATIC_DIR, 'aluminio_epr_ou_xlpe.csv'),
        'XLPE': os.path.join(
            STATIC_DIR, 'aluminio_epr_ou_xlpe.csv')
    }
}

TENSION_FALL_TABLE = os.path.join(STATIC_DIR, 'tension_fall.csv')

TEMPERATURE_TABLE = {
    'ambiente': os.path.join(
        STATIC_DIR, 'temperature_correction_ambient.csv'),
    'solo': os.path.join(
        STATIC_DIR, 'temperature_correction_ground.csv')
}

GROUPING_TABLE = os.path.join(STATIC_DIR, 'agrupamento.csv')
