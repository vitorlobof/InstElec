from typing import Dict, Self

import numpy as np

from .simultaneity_factor import simultaneity_factor
from ..settings import ureg, VOLTAGE_FF, VOLTAGE_FN
from ..PowerTriangle import PowerTriangle


class Engine:
    def __init__(
        self,
        power_phasor: PowerTriangle,
        phase_num: int,
        efficiency: float = None
    ) -> None:
        assert efficiency is None or\
            (isinstance(efficiency, (int, float)) and 0 <= efficiency <= 1),\
            'A eficiência deve ser um número de 0 a 1.'

        self.power = power_phasor
        self.phase_num = phase_num
        self.efficiency = efficiency

    def __repr__(self) -> str:
        string = [
            f'Active power: {round(self.power.active(), 2)}',
            f'Reactive power: {round(self.power.reactive(), 2)}',
            f'Phase num: {self.phase_num}',
            f'Efficiency: {self.efficiency}'
        ]
        return '\n'.join(string)

    @classmethod
    def from_axis_power(
        cls,
        axis_power: ureg.Quantity,
        phase_num: int,
        power_factor: float,
        efficiency: float,
    ):
        """
        Instancia a classe através da potência de eixo do motor.
        """
        assert isinstance(power_factor, (int, float))\
            and 0 <= power_factor <= 1,\
            'A potência deve ser um número entre 0 e 1.'

        phasor = PowerTriangle(
            axis_power.to('kW') / (efficiency * power_factor),
            power_factor
        )
        cls.axis_power = axis_power
        return cls(phasor, phase_num, efficiency=efficiency)

    @classmethod
    def from_nominal_power(
        cls,
        nominal_power: ureg.Quantity,
        utilization_factor: float,
        phase_num: int,
        power_factor: float,
        efficiency: float
    ) -> Self:
        """
        Instancia a classe através potência nominal e o fator de utilização
        do motor.
        """
        assert isinstance(utilization_factor, float)\
            and 0 <= utilization_factor <= 1,\
            'O fator de utilização deve ser um número entre 0 e 1.'

        axis_power = nominal_power * utilization_factor
        return cls.from_axis_power(
            axis_power,
            power_factor,
            phase_num,
            efficiency=efficiency
        )

    def demand(self) -> ureg.Quantity:
        """
        Returns the demand of the engine. Which corresponds to
        the active power of the engine power triangle.
        """
        return self.power.active()

    def current(self) -> ureg.Quantity:
        """
        Calcula a corrente que passa pelo motor.
        """
        active = self.power.active()
        pf = self.power.power_factor()

        if self.phase_num == 1:
            current = active/(VOLTAGE_FN*pf)
        elif self.phase_num == 2:
            current = active/(VOLTAGE_FF*pf)
        elif self.phase_num == 3:
            current = active/(np.sqrt(3)*VOLTAGE_FF*pf)
        else:
            current = active/(self.phase_num*VOLTAGE_FN*pf)

        return current.to_base_units()


class EngineGroup:
    def __init__(self, engines_count: Dict[Engine, int]) -> None:
        assert isinstance(engines_count, dict),\
            'The engines count has to be a dict.'

        self.power = 0
        self.phase_num = 1
        for eng, count in engines_count.items():
            assert isinstance(eng, Engine),\
                'Every key in the engines count must be an instance of Engine.'
            assert isinstance(count, int) and count >= 1,\
                'The number of engines has to be a positive integer.'

            sf = simultaneity_factor(count, eng.power.active())
            self.power += count * eng.power * sf

            self.phase_num = max(self.phase_num, eng.phase_num)

        self.engines_count = engines_count

    def __iter__(self) -> Engine:
        """
        Yields each engine in the group, including repetitions.
        """
        for engine, count in self.engines_count.items():
            for _ in range(count):
                yield engine

    def __len__(self) -> int:
        """
        Returns the number of engines in the group.
        """
        return sum(self.engines_count.values())

    def demand(self) -> ureg.Quantity:
        """
        Calculates and returns the demand of the group
        of engines.
        """
        return self.power.active()

    def current_per_phase(self) -> list:
        """
        Calculates the current that goes in each phase.
        Returns a list with the current in each fase in
        decreasing order.
        """
        phases = [0]*self.phase_num
        for eng in self:
            for i in range(eng.phase_num):
                phases[i] += eng.current()
            phases.sort()
        
        return phases

    def charge_current(self) -> ureg.Quantity:
        """
        Calculates the charge current. The highest current
        between the phases.
        """
        # The phases are sorted in increasing order. The
        # last term is the bigger.
        return self.current_per_phase()[-1]
