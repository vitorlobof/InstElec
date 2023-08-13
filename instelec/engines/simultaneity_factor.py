"""
Here to calculate the simultaneity factor that will be
used by the EngineGroup class.
"""

import os
import pandas as pd
import numpy as np
from ..settings import ureg, SIMULTANEITY_TABLE


class OutOfRangeError(Exception):
    """
    Levantado quando a potência não se encontra em nenhum dos
    intervalos para os quais a tabela tem valores.
    """


def simultaneity_factor(
    num_of_engines: int,
    axis_power: ureg.Quantity
) -> float:
    """
    Returns the simultaneity factor.
    """
    if num_of_engines == 1:
        return 1.0

    table = pd.read_excel(SIMULTANEITY_TABLE)

    column = get_column(table, num_of_engines)
    row = get_row(table, axis_power)

    return table.loc[row, column]


def get_column(table: pd.DataFrame, num_of_engines: int):
    """
    Seleciona a coluna com base na quantidade de motores.
    """
    for value in table.columns[2:]:
        if num_of_engines <= value:
            return value
    return value


def get_row(
    table: pd.DataFrame,
    axis_power: ureg.Quantity
) -> int:
    """
    Seleciona a linha por meio da potência de eixo.
    """
    axis_power = axis_power.to(ureg.horsepower).magnitude

    for idx, row in table.iterrows():
        inf_limit = row['inf_limit (HP)']
        sup_limit = row['sup_limit (HP)']

        if np.isnan(sup_limit):
            sup_limit = float('inf')

        if inf_limit <= axis_power <= sup_limit:
            return idx

    raise OutOfRangeError('Este valor para a potência de eixo não é tabelado.')
