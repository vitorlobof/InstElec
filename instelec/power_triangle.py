"""
Here the PowerTriangle class is implemented, it is the main way
for this module to deal with power and will be used on multiple
other parts of the module.
"""

from typing import Self
import numpy as np
from .settings import ureg


class PowerTriangle(complex):
    """
    Receives two powers of the power triangle or one power
    and the power factor.
    """
    def __new__(cls, power: ureg.Quantity, power_factor: float):
        assert isinstance(power_factor, (int, float)) and 0 <= power_factor <= 1,\
            'The power factor has to be a number from 0 to 1.'

        cos = power_factor
        sin = np.sqrt(1 - power_factor**2)

        if power.units == ureg.Unit('kVA'):
            real, imag = power.magnitude*cos, power.magnitude*sin
        elif power.units == ureg.Unit('kW'):
            real, imag = power.magnitude, power.magnitude*(sin/cos)
        elif power.units == ureg.Unit('kvar'):
            real, imag = power.magnitude*(cos/sin), power.magnitude
        else:
            raise ValueError(
                'A potência só pode apresentar as unidades kVA, kW ou kvar.')

        return super(PowerTriangle, cls).__new__(cls, real, imag)

    def __str__(self) -> str:
        parts = (
            f'Apparent power = {self.apparent}',
            f'Active power = {self.active}',
            f'Reactive power = {self.reactive}'
        )
        return f'<{", ".join(parts)}>'

    def __repr__(self) -> str:
        return "\n".join((
            f'Apparent power = {self.apparent}',
            f'Active power = {self.active}',
            f'Reactive power = {self.reactive}'
        ))

    def __neg__(self) -> Self:
        val = super().__neg__()
        return super().__new__(type(self), val.real, val.imag)

    def __add__(self, other) -> Self:
        val = super().__add__(other)
        return super().__new__(type(self), val.real, val.imag)

    def __radd__(self, other) -> Self:
        val = super().__radd__(other)
        return super().__new__(type(self), val.real, val.imag)

    def __sub__(self, other) -> Self:
        val = super().__sub__(other)
        return super().__new__(type(self), val.real, val.imag)

    def __rsub__(self, other) -> Self:
        val = super().__rsub__(other)
        return super().__new__(type(self), val.real, val.imag)

    def __mul__(self, other) -> Self:
        val = super().__mul__(other)
        return super().__new__(type(self), val.real, val.imag)

    def __rmul__(self, other) -> Self:
        val = super().__rmul__(other)
        return super().__new__(type(self), val.real, val.imag)

    def __pow__(self, other) -> Self:
        val = super().__pow__(other)
        return super().__new__(type(self), val.real, val.imag)

    @property
    def apparent(self) -> float:
        """
        Returns the apparent power.
        """
        return abs(self)*ureg.Unit('kVA')

    @property
    def active(self) -> float:
        """
        Returns the active power.
        """
        return self.real*ureg.Unit('kW')

    @property
    def reactive(self) -> float:
        """
        Returns the reactive power.
        """
        return self.imag*ureg.Unit('kvar')

    @property
    def power_factor(self) -> float:
        """
        Returns the power factor. In other words, the cossine
        of the power triangle.
        """
        return self.real/abs(self)

    def inductive_power_factor_to(self, power_factor: float) -> ureg.Quantity:
        """
        Calculates and returns the power the capacitive bank
        requires to correct the power factor to the given
        power_factor.
        """
        assert isinstance(power_factor, (int, float)
                          ), 'The power_factor has to be a number from 0 to 1.'
        assert 0 <= power_factor <= 1, 'The power_factor has to be a number from 0 to 1.'

        tan = np.sqrt(1/power_factor**2 - 1)
        return (self.active*tan).to(ureg.Unit('kvar')) - self.reactive

    def capacitive_power_factor_to(self, power_factor: float) -> ureg.Quantity:
        """
        Calculates and returns the power the capacitive bank
        requires to correct the power factor to the given
        power_factor.
        """
        assert isinstance(power_factor, (int, float)
                          ), 'The power_factor has to be a number from 0 to 1.'
        assert 0 <= power_factor <= 1, 'The power_factor has to be a number from 0 to 1.'

        tan = - np.sqrt(1/power_factor**2 - 1)
        return (self.active*tan).to(ureg.Unit('kvar')) - self.reactive

    def power_factor_to(self, power_factor: float) -> (ureg.Quantity, ureg.Quantity):
        """
        Returns the range of values for the reactive power that
        could be added to make the power factor bigger or equal
        to the given value.
        """
        return (
            self.capacitive_power_factor_to(power_factor),
            self.inductive_power_factor_to(power_factor)
        )
