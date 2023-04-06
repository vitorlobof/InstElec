from ..settings import ureg, VOLTAGE_FF, VOLTAGE_FN
import numpy as np
from .tables import Amperage, TensionFall, NotInTableError

class CondutorSection:
    def __init__(
        self,
        material: str,
        insulator: str,
        instalation_method: str,
        power_factor: float,
        phase_num: int
    ) -> None:
        assert isinstance(power_factor, float) and 0 <= power_factor <= 1, 'O fator de potência tem que ser um número de 0 a 1.'
        assert phase_num in {1, 3}, 'O motor deve ser monofásico ou trifásico.'

        self.method = instalation_method
        self.power_factor = power_factor
        self.phase_num = phase_num

        self.ampacity = Ampacity(material, insulator)
        self.tension_fall = TensionFall()
    
    def by_amperage(
            self, current: ureg.Quantity) -> ureg.Quantity:
        return self.amperage.get_section(
            current, self.method, self.phase_num)
    
    def nominal_current(
            self, section: ureg.Quantity) -> ureg.Quantity:
        return self.ampacity.get_nominal_current(
            section, self.method, self.phase_num)
    
    def by_tension_fall_simple(
        self,
        current: ureg.Quantity,
        distance: ureg.Quantity,
        max_fall: float
    ) -> ureg.Quantity:
        vff = VOLTAGE_FF.to(ureg.volt).magnitude
        vfn = VOLTAGE_FN.to(ureg.volt).magnitude
        d = distance.to(ureg.meter).magnitude
        i = current.to(ureg.ampere).magnitude

        if self.phase_num == 1:
            section = (2*(1/56)*(d*i))/(max_fall*vfn)
        elif self.phase_num == 3:
            section = (np.sqrt(3)*(1/56)*(d*i))/(max_fall*vff)
        
        return section * ureg.millimeter**2
    
    def by_tension_fall(
        self,
        current: ureg.Quantity,
        distance: ureg.Quantity,
        max_fall: float
    ) -> ureg.Quantity:
        vff = VOLTAGE_FF
        vfn = VOLTAGE_FN

        if self.by_ampacity(current) <= 25*ureg.millimeter**2:
            result = self.by_tension_fall_simple(
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
        fault_elimination_time: ureg.Quantity,
        min_temperature: float,
        max_temperature: float
    ) -> ureg.Quantity:
        result = 1/0.34 * ureg.millimeter**2/(ureg.kiloampere * ureg.second**(1/2))
        result *= np.sqrt(fault_elimination_time)
        result *= simmetric_short_circuit_current
        result /= np.sqrt(np.log10((234 + max_temperature)/(234 + min_temperature)))

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

class CupperPVC(CondutorSection):
    def __init__(
        self,
        instalation_method: str,
        power_factor: float,
        phase_num: int
    ) -> None:
        super().__init__(
            'cupper',
            'PVC',
            instalation_method,
            power_factor,
            phase_num
        )
    
    def by_short_circuit(
        self,
        simmetric_short_circuit_current: ureg.Quantity,
        fault_elimination_time: ureg.Quantity,
    ) -> ureg.Quantity:
        return super().by_short_circuit(
            simmetric_short_circuit_current,
            fault_elimination_time,
            70,
            160
        )

class CupperEPR(CondutorSection):
    def __init__(
        self,
        instalation_method: str,
        power_factor: float,
        phase_num: int
    ) -> None:
        super().__init__(
            'cupper',
            'EPR',
            instalation_method,
            power_factor,
            phase_num
        )
    
    def by_short_circuit(
        self,
        simmetric_short_circuit_current: ureg.Quantity,
        fault_elimination_time: ureg.Quantity,
    ) -> ureg.Quantity:
        return super().by_short_circuit(
            simmetric_short_circuit_current,
            fault_elimination_time,
            90,
            250
        )

class CupperXLPE(CupperEPR):
    pass
