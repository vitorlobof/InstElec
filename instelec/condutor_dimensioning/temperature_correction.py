from ..settings import TEMPERATURE_TABLE

class TemperatureCorrection:
    place = None

    def __init__(self, insulator) -> None:
        filepath = TEMPERATURE_TABLE[self.place]
        self.table = (
            pd.read_csv(filepath, index_col='temperatura')
            .astype('float16')
        )
        self.insulator = insulator
    
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

class TemperatureCorrectionAmbient(TemperatureCorrection):
    place = 'ambiente'

class TemperatureCorrectionGround(TemperatureCorrection):
    place = 'solo'
