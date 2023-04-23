from ..settings import TEMPERATURE_TABLE

class TemperatureCorrection:
    insulator = None
    place = None

    def __init__(self) -> None:
        filepath = TEMPERATURE_TABLE[self.place]
        self.table = (
            pd.read_csv(filepath, index_col='temperatura')
            .astype('float16')
        )
    
    def correction_factor(
            self, temperature: ureg.Quantity) -> float:
        series = self.table[self.insulator]
        for value, factor in series.items():
            if value >= temperature:
                if factor == np.nan:
                    break
                return factor

        raise NotInTableError(
            'O isolante utilizado não suporta essa temperatura.')

class Ambient(TemperatureCorrection):
    place = 'ambiente'

class Ground(TemperatureCorrection):
    place = 'solo'

class AmbientPVC(Ambient):
    insulator = 'PVC'

class AmbientEPR(Ambient):
    insulator = 'EPR'

class AmbientXLPE(Ambient):
    insulator = 'XLPE'