"""
Here are defined the classes that will actually calculate the
sections of the conductors of the electrical instalation.
"""

from typing import Self
import numpy as np
from ..settings import ureg, VOLTAGE_FF, VOLTAGE_FN
from .tables import (
    Amperage, VoltageDrop, NotInTableError, Grouping
)
from .temperature_correction import TemperatureCorrectionAmbient


def above_min_section(func):
    """
    A decorator to garantee any section outputed will be
    bigger or equal to the min_section.
    """

    def wrapper(self, *args, **kwargs):
        section = func(self, *args, **kwargs)
        return max(section, self.min_section)

    return wrapper


class CondutorSection:
    """
    This is an abstract class to be that will be composed with
    a class to define the properties of the wire material and
    other to define the properties of the insulator used. It
    defines all the forms to calculate the section of a condutor.
    """
    material: str
    electrical_resistivity: ureg.Quantity

    insulator: str

    continuous_service_max_temperature: ureg.Quantity
    overcharge_limit_temperature: ureg.Quantity
    sc_limit_temperature: ureg.Quantity

    # Meant to set the minimum value for a section, it depends
    # on the material used and  will be used by the
    # above_min_section decorator.
    min_section: ureg.Quantity

    def __init__(
        self,
        instalation_method: str,
        power_factor: float,
        phase_num: int
    ) -> None:
        assert isinstance(
            power_factor, float) and 0 <= power_factor <= 1,\
            'O fator de potência tem que ser um número de 0 a 1.'
        assert phase_num in {1, 3}, 'O motor deve ser monofásico ou trifásico.'

        self.method = instalation_method
        self.power_factor = power_factor
        self.phase_num = phase_num

        self.amperage = Amperage(self.material, self.insulator)
        self.voltage_drop = VoltageDrop()

    def __repr__(self) -> str:
        string = [
            f'Material: {self.material}',
            f'Insulator: {self.insulator}',
            f'Instalation method: {self.method}',
            f'Power factor: {self.power_factor}',
            f'Phase number: {self.phase_num}'
        ]
        return '\n'.join(string)

    def grouping_correction(self, num_of_circuits: int) -> Self:
        """
        Applies gruping factor to the amperage table.
        """
        self.amperage.table *= Grouping(
            self.method, num_of_circuits).correction_factor()
        return self

    def temperature_correction(self, temperature: ureg.Quantity) -> Self:
        """
        Applies the temperature correction factor to the amperage
        table.
        """
        self.amperage.table *= TemperatureCorrectionAmbient(
            self.insulator).correction_factor(temperature)
        return self

    @above_min_section
    def by_amperage(
            self, current: ureg.Quantity) -> ureg.Quantity:
        """
        Calculates the section of the conductor by the amperage
        method.
        """
        return self.amperage.get_section(
            current, self.method, self.phase_num)

    def nominal_current(
            self, section: ureg.Quantity) -> ureg.Quantity:
        """
        Returns the nominal current. The biggest current a
        section supports considering the amperage table.
        """
        return self.amperage.get_nominal_current(
            section, self.method, self.phase_num)

    def by_voltage_drop_simple(
        self,
        current: ureg.Quantity,
        distance: ureg.Quantity,
        max_fall: float
    ) -> ureg.Quantity:
        """
        Calculates the section by the voltage drop method.
        It should not be used by the user directly, it's here
        to by called by the by_voltage_drop method.
        """
        if self.phase_num == 1:
            section = (2*self.electrical_resistivity *
                       distance*current)/(max_fall*VOLTAGE_FN)
        elif self.phase_num == 3:
            section = (np.sqrt(3)*self.electrical_resistivity *
                       distance*current)/(max_fall*VOLTAGE_FF)
        else:
            raise NotImplementedError(
                "Was only implemented for phase_num equals 1 or 3.")

        return section.to(ureg.millimeter**2)

    @above_min_section
    def by_voltage_drop(
        self,
        current: ureg.Quantity,
        distance: ureg.Quantity,
        max_fall: float
    ) -> ureg.Quantity:
        """
        Calculates the section by the voltage drop method.
        """

        if self.by_amperage(current) <= 25*ureg.millimeter**2:
            result = self.by_voltage_drop_simple(
                current, distance, max_fall)

            for section in self.amperage.table.index:
                if result.magnitude <= section:
                    return section * ureg.millimeter**2

        for idx, row in self.voltage_drop.table.iterrows():
            cos = self.power_factor
            sin = np.sqrt(1 - cos**2)

            current = current.to(ureg.ampere)
            distance = distance.to(ureg.meter)

            fall = np.sqrt(3)*current*distance
            fall *= row.R*cos + row.X*sin
            fall /= 10*1*VOLTAGE_FF

            if fall.magnitude <= 100*max_fall:
                return idx*ureg.millimeter**2

        raise NotInTableError('Não corresponde a nenhuma seção tabelada.')

    @above_min_section
    def by_short_circuit(
        self,
        simmetric_short_circuit_current: ureg.Quantity,
        fault_elimination_time: ureg.Quantity
    ) -> ureg.Quantity:
        """
        Calculates the section by the short_circuit method.
        """

        min_temp = self.continuous_service_max_temperature.magnitude
        max_temp = self.sc_limit_temperature.magnitude

        result = 1/0.34 * ureg.millimeter**2 / \
            (ureg.kiloampere * ureg.second**(1/2))
        result *= np.sqrt(fault_elimination_time)
        result *= simmetric_short_circuit_current
        result /= np.sqrt(np.log10((234 + max_temp)/(234 + min_temp)))

        result = result.to(ureg.millimeter**2)

        for section in self.amperage.table.index:
            if result.magnitude <= section:
                return section*ureg.millimeter**2

        raise NotInTableError('Não corresponde a nenhuma seção tabelada.')

    def protection_condutor(
            self, phase_section: ureg.Quantity) -> ureg.Quantity:
        """
        Receives the section choosen to the phase condutor and
        returns the section of the protection condutor.
        """

        if phase_section <= 16 * ureg.millimeter**2:
            result = phase_section
        elif phase_section <= 35 * ureg.millimeter**2:
            result = 16 * ureg.millimeter**2
        else:
            result = 0.5 * phase_section

        for section in self.amperage.table.index:
            if result.magnitude <= section:
                return section*ureg.millimeter**2

        raise NotInTableError('Não corresponde a nenhuma seção tabelada.')


class Cupper:
    """
    Defines the properties of a cupper wire.
    """

    material = 'cupper'
    electrical_resistivity = 1/56*10**(-6)*(ureg.ohm*ureg.meter)

    # Just add the lights kwarg to the __init__ method for it
    # be used by the min_section property.
    def __init__(
        self,
        instalation_method: str,
        power_factor: float,
        phase_num: int,
        lights: bool = False
    ) -> None:
        super().__init__(
            instalation_method,
            power_factor,
            phase_num
        )

        self.lights = lights

    @property
    def min_section(self):
        """
        Property that gives the min_section that
        a cupper wire could have.
        """
        if self.lights:
            return 1.5 * ureg.millimeter**2

        return 2.5 * ureg.millimeter**2


class Aluminium:
    """
    Defines the properties of an aluminium wire.
    """

    material = 'aluminium'
    electrical_resistivity = 2.82*10**(-8)*(ureg.ohm*ureg.meter)

    min_section = 16 * ureg.millimeter**2


class PVC:
    """
    Defines the properties of a wire isolated by PVC.
    """

    insulator = 'PVC'

    continuous_service_max_temperature = ureg.Quantity(70, 'celsius')
    overcharge_limit_temperature = ureg.Quantity(100, 'celsius')
    sc_limit_temperature = ureg.Quantity(160, 'celsius')


class EPR:
    """
    Defines the properties of a wire isolated by EPR.
    """

    insulator = 'EPR'

    continuous_service_max_temperature = ureg.Quantity(90, 'celsius')
    overcharge_limit_temperature = ureg.Quantity(130, 'celsius')
    sc_limit_temperature = ureg.Quantity(250, 'celsius')


class XLPE:
    """
    Defines the properties of a wire isolated by XLPE.
    """

    insulator = 'XLPE'

    continuous_service_max_temperature = ureg.Quantity(90, 'celsius')
    overcharge_limit_temperature = ureg.Quantity(130, 'celsius')
    sc_limit_temperature = ureg.Quantity(250, 'celsius')


class CupperPVC(Cupper, PVC, CondutorSection):
    """
    Class used to calculate the section of a cupper wire
    isolated with PVC.
    """


class CupperEPR(Cupper, EPR, CondutorSection):
    """
    Class used to calculate the section of a cupper wire
    isolated with EPR.
    """


class CupperXLPE(Cupper, XLPE, CondutorSection):
    """
    Class used to calculate the section of a cupper wire
    isolated with XLPE.
    """


class AluminiumPVC(Aluminium, PVC, CondutorSection):
    """
    Class used to calculate the section of a aluminium wire
    isolated with PVC.
    """


class AluminiumEPR(Aluminium, EPR, CondutorSection):
    """
    Class used to calculate the section of a aluminium wire
    isolated with EPR.
    """


class AluminiumXLPE(Aluminium, XLPE, CondutorSection):
    """
    Class used to calculate the section of a aluminium wire
    isolated with XLPE.
    """
