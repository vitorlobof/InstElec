from ..settings import ureg, VOLTAGE_FF, VOLTAGE_FN
import numpy as np
from .tables import (
    Amperage, VoltageDrop, NotInTableError, Grouping
)
from .temperature_correction import TemperatureCorrectionAmbient

class CondutorSection:
    material: str = None
    electrical_conductivity: ureg.Quantity = None
    
    insulator: str = None

    continuous_service_max_temperature = None
    overcharge_limit_temperature = None
    sc_limit_temperature = None

    def __init__(
        self,
        instalation_method: str,
        power_factor: float,
        phase_num: int
    ) -> None:
        assert isinstance(power_factor, float) and 0 <= power_factor <= 1, 'O fator de potência tem que ser um número de 0 a 1.'
        assert phase_num in {1, 3}, 'O motor deve ser monofásico ou trifásico.'

        self.method = instalation_method
        self.power_factor = power_factor
        self.phase_num = phase_num

        self.amperage = Amperage(self.material, self.insulator)
        self.voltage_drop = VoltageDrop()
    
    def grouping_correction(self, num_of_circuits):
        cf = Grouping(
            self.method. num_of_circuits).correction_factor()
        self.table *= correction
        return self
    
    def temperature_correction(self, temperature):
        cf = TemperatureCorrectionAmbient(
            self.insulator).correction_factor(temperature)
        self.table *= correction
        return self
    
    def by_amperage(
            self, current: ureg.Quantity) -> ureg.Quantity:
        return self.amperage.get_section(
            current, self.method, self.phase_num)
    
    def nominal_current(
            self, section: ureg.Quantity) -> ureg.Quantity:
        return self.amperage.get_nominal_current(
            section, self.method, self.phase_num)
    
    def by_voltage_drop_simple(
        self,
        current: ureg.Quantity,
        distance: ureg.Quantity,
        max_fall: float
    ) -> ureg.Quantity:
        vff = VOLTAGE_FF
        vfn = VOLTAGE_FN
        L = distance
        I = current
        p = self.electrical_resistivity

        if self.phase_num == 1:
            section = (2*p*L*I)/(max_fall*vfn)
        elif self.phase_num == 3:
            section = (np.sqrt(3)*p*L*I)/(max_fall*vff)
        
        return section.to(ureg.millimeter**2)
    
    def by_voltage_drop(
        self,
        current: ureg.Quantity,
        distance: ureg.Quantity,
        max_fall: float
    ) -> ureg.Quantity:
        vff = VOLTAGE_FF
        vfn = VOLTAGE_FN

        if self.by_amperage(current) <= 25*ureg.millimeter**2:
            result = self.by_voltage_drop_simple(
                current, distance, max_fall)
            
            for section in self.amperage.table.index:
                if result.magnitude <= section:
                    return section * ureg.millimeter**2
        else:
            for idx, row in self.tension_fall.table.iterrows():
                cos = self.power_factor
                sin = np.sqrt(1 - cos**2)

                current = current.to(ureg.ampere)
                distance = distance.to(ureg.meter)
                vff = vff.to(ureg.volt)

                fall = np.sqrt(3)*current*distance
                fall *= row.R*cos + row.X*sin
                fall /= 10*1*vff
                
                if fall.magnitude <= 100*max_fall:
                    return idx*ureg.millimeter**2
            
        raise NotInTableError('Não corresponde a nenhuma seção tabelada.')
    
    def by_short_circuit(
        self,
        simmetric_short_circuit_current: ureg.Quantity,
        fault_elimination_time: ureg.Quantity
    ) -> ureg.Quantity:
        min_temp = self.continuous_service_max_temperature.magnitude
        max_temp = self.sc_limit_temperature.magnitude

        result = 1/0.34 * ureg.millimeter**2/(ureg.kiloampere * ureg.second**(1/2))
        result *= np.sqrt(fault_elimination_time)
        result *= simmetric_short_circuit_current
        result /= np.sqrt(np.log10((234 + max_temp)/(234 + min_temp)))

        result = result.to(ureg.millimeter**2)

        for section in self.ampacity.table.index:
            if result.magnitude <= section:
                return section*ureg.millimeter**2
        
        raise NotInTableError('Não corresponde a nenhuma seção tabelada.')

    def protection_condutor(self, phase_section: ureg.Quantity) -> ureg.Quantity:
        if phase_section <= 16 * ureg.millimeter**2:
            result = phase_section
        elif phase_section <= 35 * ureg.millimeter**2:
            result = 16 * ureg.millimeter**2
        else:
            result = 0.5 * phase_section
        
        for section in self.ampacity.table.index:
            if result.magnitude <= section:
                return section*ureg.millimeter**2
        
        raise NotInTableError('Não corresponde a nenhuma seção tabelada.')

class Cupper:
    material = 'cupper'
    electrical_resistivity = 1/56*10**(-6)*(ureg.ohm*ureg.meter)

    def min_section(self, lights=False) -> ureg.Quantity:
        if lights:
            return 1.5 * ureg.millimeter**2
        else:
            return 2.5 * ureg.millimeter**2

class Aluminum:
    material = 'aluminum'
    electrical_resistivity = 2.82*10**(-8)*(ureg.ohm*ureg.meter)

    def min_section(self, lights=False) -> ureg.Quantity:
        return 16 * ureg.millimeter**2

class PVC:
    insulator = 'PVC'

    continuous_service_max_temperature = ureg.Quantity(70, 'celsius')
    overcharge_limit_temperature = ureg.Quantity(100, 'celsius')
    sc_limit_temperature = ureg.Quantity(160, 'celsius')

class EPR:
    insulator = 'EPR'

    continuous_service_max_temperature = ureg.Quantity(90, 'celsius')
    overcharge_limit_temperature = ureg.Quantity(130, 'celsius')
    sc_limit_temperature = ureg.Quantity(250, 'celsius')

class XLPE:
    insulator = 'XLPE'

    continuous_service_max_temperature = ureg.Quantity(90, 'celsius')
    overcharge_limit_temperature = ureg.Quantity(130, 'celsius')
    sc_limit_temperature = ureg.Quantity(250, 'celsius')

class CupperPVC(Cupper, PVC, CondutorSection):
    pass

class CupperEPR(Cupper, EPR, CondutorSection):
    pass

class CupperXLPE(Cupper, XLPE, CondutorSection):
    pass

class AluminumPVC(Aluminum, PVC, CondutorSection):
    pass

class AluminumEPR(Aluminum, EPR, CondutorSection):
    pass

class AluminumXLPE(Aluminum, XLPE, CondutorSection):
    pass
