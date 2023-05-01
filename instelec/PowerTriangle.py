import numpy as np
from .settings import ureg

class PowerTriangle(complex):
    """
    Receives two powers of the power triangle or one power
    and the power factor.
    """
    def __new__(cls, power: ureg.Quantity, power_factor: float) -> None:
        assert isinstance(power_factor, (int, float)) and 0 <= power_factor <= 1,\
            'The power factor has to be a number from 0 to 1.'

        cos = power_factor
        sin = np.sqrt(1 - power_factor**2)

        if power.units == ureg.Unit('kVA'):
            x, y = power.magnitude*cos, power.magnitude*sin
        elif power.units == ureg.Unit('kW'):
            x, y = power.magnitude, power.magnitude*(sin/cos)
        elif power.units == ureg.Unit('kvar'):
            x, y = power.magnitude*(cos/sin), power.magnitude
        else:
            raise ValueError('A potência só pode apresentar as unidades kVA, kW ou kvar.')

        return super(PowerTriangle, cls).__new__(cls, x, y)
    
    def __neg__(self) -> 'PowerTriangle':
        val = super(PowerTriangle, self).__neg__()
        return super(PowerTriangle, self).__new__(
            type(self), val.real, val.imag)

    def __add__(self, other) -> 'PowerTriangle':
        val = super(PowerTriangle, self).__add__(other)
        return super(PowerTriangle, self).__new__(
            type(self), val.real, val.imag)
    
    def __radd__(self, other) -> 'PowerTriangle':
        val = super(PowerTriangle, self).__radd__(other)
        return super(PowerTriangle, self).__new__(
            type(self), val.real, val.imag)
    
    def __sub__(self, other) -> 'PowerTriangle':
        val = super(PowerTriangle, self).__sub__(other)
        return super(PowerTriangle, self).__new__(
            type(self), val.real, val.imag)
    
    def __rsub__(self, other) -> 'PowerTriangle':
        val = super(PowerTriangle, self).__rsub__(other)
        return super(PowerTriangle, self).__new__(
            type(self), val.real, val.imag)
    
    def __mul__(self, other) -> 'PowerTriangle':
        val = super(PowerTriangle, self).__mul__(other)
        return super(PowerTriangle, self).__new__(
            type(self), val.real, val.imag)

    def __rmul__(self, other) -> 'PowerTriangle':
        val = super(PowerTriangle, self).__rmul__(other)
        return super(PowerTriangle, self).__new__(
            type(self), val.real, val.imag)
    
    def __pow__(self, other) -> 'PowerTriangle':
        val = super(PowerTriangle, self).__pow__(other)
        return super(PowerTriangle, self).__new__(
            type(self), val.real, val.imag)
        
    def apparent(self) -> float:
        """
        Returns the apparent power.
        """
        return abs(self)*ureg.Unit('kVA')

    def active(self) -> float:
        """
        Returns the active power.
        """
        return self.real*ureg.Unit('kW')

    def reactive(self) -> float:
        """
        Returns the reactive power.
        """
        return self.imag*ureg.Unit('kvar')

    def power_factor(self) -> float:
        """
        Returns the power factor. In other words, the cossine
        of the power triangle.
        """
        return self.real/abs(self)
    
    def indutive_power_factor_to(self, power_factor: float) -> ureg.Quantity:
        """
        Calculates and returns the power the capacitive bank
        requires to correct the power factor to the given
        power_factor.
        """
        assert isinstance(power_factor, (int, float)), 'The power_factor has to be a number from 0 to 1.'
        assert 0 <= power_factor <= 1, 'The power_factor has to be a number from 0 to 1.'

        tan = np.sqrt(1/power_factor**2 - 1)
        return self.reactive() - (self.active()*tan).to(ureg.Unit('kvar'))
    
    def capacitive_power_factor_to(self, power_factor: float) -> ureg.Quantity:
        """
        Calculates and returns the power the capacitive bank
        requires to correct the power factor to the given
        power_factor.
        """
        assert isinstance(power_factor, (int, float)), 'The power_factor has to be a number from 0 to 1.'
        assert 0 <= power_factor <= 1, 'The power_factor has to be a number from 0 to 1.'

        tan = np.sqrt(1/power_factor**2 - 1)
        return self.reactive() + (self.active()*tan).to(ureg.Unit('kvar'))
