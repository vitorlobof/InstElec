"""
Creates the TemperatureCorrection class to access the
respective table.
"""

import pandas as pd
import numpy as np
from ..settings import TEMPERATURE_TABLE, ureg
from .exceptions import NotInTableError


class TemperatureCorrection:
    """
    Accesses the temperature correction table.
    """

    place = None

    def __init__(self, insulator) -> None:
        filepath = TEMPERATURE_TABLE[self.place]
        self.table = (
            pd.read_csv(filepath, index_col='temperatura')
            .astype('float16')
        )
        self.insulator = insulator

    def correction_factor(
            self, temperature: ureg.Quantity) -> float:
        """
        Returns the temperature correcion factor.
        """
        temperature = temperature.to('celsius').magnitude
        series = self.table[self.insulator]
        for value, factor in series.items():
            if value >= temperature:
                if factor == np.nan:
                    break
                return factor

        raise NotInTableError(
            'O isolante utilizado não suporta essa temperatura.')


class TemperatureCorrectionAmbient(TemperatureCorrection):
    """
    Just meant to specify the place.
    """
    place = 'ambiente'


class TemperatureCorrectionGround(TemperatureCorrection):
    """
    Just meant to specify the place.
    """
    place = 'solo'
