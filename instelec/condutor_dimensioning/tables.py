import os
import pandas as pd
import numpy as np
from ..settings import (
    ureg, AMPERAGE_TABLE, TENSION_FALL_TABLE,
    TEMPERATURE_TABLE, GROUPING_TABLE
)

class NotInTableError(Exception):
    pass

class Amperage:
    # Traduz o número de fase para o número de condutores
    # relacionados e ela.
    CONDUCTORS_NUM = {1: 2, 3: 3}

    def __init__(self, material: str, insulator: str) -> None:
        filepath = AMPERAGE_TABLE[material][insulator]
        self.table = (
            pd.read_csv(filepath, index_col='nominal_sections')
            .astype('float16')
        )
    
    def apply_correction_factors(self, *factors):
        """
        Aplica os fatores de correção à tabela de ampacidade.
        """
        correction = 1
        for factor in factors:
            correction *= factor
        
        self.table *= correction
        return self

    def get_section(
        self,
        current: ureg.Quantity,
        instalation_method: str,
        phase_num: int
    ) -> ureg.Quantity:
        """
        Acessa a tabela de ampacidade e, através do método de
        instalação e corrente elétrica que passa pelo cabo,
        escolhe a secção do condutor.
        """
        condutors_num = phase_num
        if condutors_num == 1:
            condutors_num = 2
        col = f'{instalation_method}_{condutors_num}'

        current = current.to(ureg.ampere).magnitude
        series = self.table[col]
        for idx, value in series.items():
            if current <= value:
                return idx*ureg.millimeter**2

        raise NotInTableError(
            'A corrente é alta demais, não se encontra na tabela.')
    
    def get_nominal_current(
        self,
        section: ureg.Quantity,
        instalation_method: str,
        phase_num: int
    ) -> ureg.Quantity:
        """
        Retorna a corrente nominal, a máxima corrente que o
        condutor escolhido suporta.
        """
        condutors_num = phase_num
        if condutors_num == 1:
            condutors_num = 2
        col = f'{instalation_method}_{condutors_num}'

        nominal_current = self.table.loc[section.magnitude, col]
        return nominal_current * ureg.ampere

class TensionFall:
    def __init__(self) -> None:
        filepath = TENSION_FALL_TABLE
        self.table = (
            pd.read_csv(filepath, index_col='section')
            .astype('float16')
        )

class Temperature:
    def __init__(self,
        temperature: ureg.Quantity,
        place: str
    ) -> None:
        filepath = TEMPERATURE_TABLE[place]
        self.table = (
            pd.read_csv(filepath, index_col='temperatura')
            .astype('float16')
        )
    
    def correction_factor(self) -> float:
        temperature = self.temperature.to(ureg.celsius).magnitude
        series = self.temp_table[self.isolation]
        for value, factor in series.items():
            if value >= temperatura:
                if factor == np.nan:
                    break
                return round(factor, 2)

        raise NotInTableError(
            'O isolante utilizado não suporta essa temperatura.')

class Grouping:
    def __init__(self, num_circuits: int, method: str) -> None:
        filepath = GROUPING_TABLE
        self.table = pd.read_csv(filepath)
        self.table.index += 1
        
        self.num_circuits = num_circuits
        self.method = method
    
    def correction_factor(self) -> float:
        return self.table.loc[self.num_circuits, self.method]