import numpy as np
from .settings import ureg

class PowerPhasor(complex):
    """
    Receives two powers of the power triangle or one power
    and the power factor.
    """
    def __new__(cls, power: ureg.Quantity, power_factor: float) -> None:
        assert isinstance(power_factor, (int, float)) and 0 <= power_factor <= 1,\
            'The power factor has to be a number from 0 to 1.'

        cos = power_factor
        sin = np.sqrt(1 - power_factor**2)

        power = power.to_base_units()

        if power.units == ureg.Unit('VA'):
            x, y = power.to('kVA').magnitude*cos, power.magnitude*sin
        elif power.units == ureg.Unit('W'):
            x, y = power.to('kW').magnitude, power.magnitude*(sin/cos)
        elif power.units == ureg.Unit('var'):
            x, y = power.to('kvar').magnitude*(cos/sin), power.magnitude
        else:
            raise ValueError('A potência só pode apresentar as unidades VA, W ou var.')

        return super(PowerPhasor, cls).__new__(cls, x, y)
    
    def __neg__(self) -> 'PowerPhasor':
        val = super(PowerPhasor, self).__neg__()
        return super(PowerPhasor, self).__new__(
            type(self), val.real, val.imag)

    def __add__(self, other) -> 'PowerPhasor':
        val = super(PowerPhasor, self).__add__(other)
        return super(PowerPhasor, self).__new__(
            type(self), val.real, val.imag)
    
    def __radd__(self, other) -> 'PowerPhasor':
        val = super(PowerPhasor, self).__radd__(other)
        return super(PowerPhasor, self).__new__(
            type(self), val.real, val.imag)
    
    def __sub__(self, other) -> 'PowerPhasor':
        val = super(PowerPhasor, self).__sub__(other)
        return super(PowerPhasor, self).__new__(
            type(self), val.real, val.imag)
    
    def __rsub__(self, other) -> 'PowerPhasor':
        val = super(PowerPhasor, self).__rsub__(other)
        return super(PowerPhasor, self).__new__(
            type(self), val.real, val.imag)
    
    def __mul__(self, other) -> 'PowerPhasor':
        val = super(PowerPhasor, self).__mul__(other)
        return super(PowerPhasor, self).__new__(
            type(self), val.real, val.imag)

    def __rmul__(self, other) -> 'PowerPhasor':
        val = super(PowerPhasor, self).__rmul__(other)
        return super(PowerPhasor, self).__new__(
            type(self), val.real, val.imag)
    
    def __pow__(self, other) -> 'PowerPhasor':
        val = super(PowerPhasor, self).__pow__(other)
        return super(PowerPhasor, self).__new__(
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
        return self.imag*ureg.Unit('kVAr')

    def power_factor(self) -> float:
        """
        Returns the power factor. In other words, the cossine
        of the power triangle.
        """
        return self.real/abs(self)
    
    def indutive_power_factor_to(self, power_factor: float) -> float:
        """
        Calculates and returns the power the capacitive bank
        requires to correct the power factor to the given
        power_factor_indutive.
        """
        assert isinstance(power_factor_indutive, (int, float)),\
            'The power_factor_indutive has to be a number from 0 to 1.'
        assert 0 <= power_factor_indutive <= 1,\
            'The power_factor_indutive has to be a number from 0 to 1.'

        tan = np.sqrt(1/power_factor_indutive**2 - 1)
        return (self.reactive() - self.active()*tan)*ureg.Unit('kVAr')
    
    def capacitive_power_factor_to(self, power_factor: float) -> float:
        """
        Calculates and returns the power the capacitive bank
        requires to correct the power factor to the given
        power_factor_capacitive.
        """
        assert isinstance(power_factor_capacitive, (int, float)),\
            'The power_factor_capacitive has to be a number from 0 to 1.'
        assert 0 <= power_factor_capacitive <= 1,\
            'The power_factor_capacitive has to be a number from 0 to 1.'

        tan = np.sqrt(1/power_factor_capacitive**2 - 1)
        return (self.reactive() + self.active()*tan)*ureg.Unit('kVAr')
