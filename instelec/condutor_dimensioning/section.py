from ..settings import ureg, VOLTAGE_FF, VOLTAGE_FN
import numpy as np
from .tables import Amperage, TensionFall, NotInTableError

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
        self.tension_fall = TensionFall()
    
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
        p = self.electrical_conductivity

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

        if self.by_ampacity(current) <= 25*ureg.millimeter**2:
            result = self.by_voltage_drop_simple(
                current, distance, max_fall)
            
            for section in self.ampacity.table.index:
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

class Cupper(CondutorSection):
    material = 'cupper'
    electrical_conductivity = 1/56*10**(-6)*(ureg.ohm*ureg.meter)

    def min_section(self, adm=False) -> ureg.Quantity:
        if adm:
            return 1.5 * ureg.millimeter**2
        else:
            return 2.5 * ureg.millimeter**2

class CupperPVC(Cupper):
    insulator = 'PVC'

    continuous_service_max_temperature = 70*ureg.Unit('celsius')
    overcharge_limit_temperature = 100*ureg.Unit('celsius')
    sc_limit_temperature = 160*ureg.Unit('celsius')

class CupperEPR(Cupper):
    insulator = 'EPR'

    continuous_service_max_temperature = 90*ureg.Unit('celsius')
    overcharge_limit_temperature = 130*ureg.Unit('celsius')
    sc_limit_temperature = 250*ureg.Unit('celsius')

class CupperXLPE(Cupper):
    insulator = 'XLPE'

    continuous_service_max_temperature = 90*ureg.Unit('celsius')
    overcharge_limit_temperature = 130*ureg.Unit('celsius')
    sc_limit_temperature = 250*ureg.Unit('celsius')
