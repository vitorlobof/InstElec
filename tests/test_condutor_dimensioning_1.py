import unittest
import instelec as ie
u = ie.ureg


class TestCondutorDimensioning(unittest.TestCase):
    def setUp(self):
        self.eng1 = ie.Engine(ie.PowerTriangle(8*u.kilovolt_ampere, 0.8), 1)
        self.eng2 = ie.Engine(ie.PowerTriangle(35*u.kilovolt_ampere, 0.7), 3)
        self.eng3 = ie.Engine(ie.PowerTriangle(11*u.kilovolt_ampere, 0.8), 1)
        self.eng4 = ie.Engine(ie.PowerTriangle(26*u.kilovolt_ampere, 0.7), 3)
        self.eng5 = ie.Engine(ie.PowerTriangle(17.2*u.kilovolt_ampere, 0.7), 1)
        self.eng6 = ie.Engine(ie.PowerTriangle(28*u.kilovolt_ampere, 0.7), 3)
        self.eng7 = ie.Engine(ie.PowerTriangle(12.2*u.kilovolt_ampere, 0.8), 1)

        self.ccm1 = ie.EngineGroup({self.eng1: 1, self.eng2: 1, self.eng3: 1})
        self.ccm2 = ie.EngineGroup({self.eng4: 1, self.eng3: 1, self.eng5: 1})
        self.qdtl = ie.EngineGroup({self.eng1: 1, self.eng6: 1, self.eng7: 1})

        self.ccm2_section = ie.CupperPVC(
            'B1',
            self.ccm2.power.power_factor,
            self.ccm2.phase_num
        )

    def test_currents(self):
        self.assertAlmostEqual(self.eng1.current(), 36.364*u.ampere, places=3)
        self.assertAlmostEqual(self.eng2.current(), 53.177*u.ampere, places=3)
        self.assertAlmostEqual(self.eng3.current(), 50.000*u.ampere, places=3)
        self.assertAlmostEqual(self.eng4.current(), 39.503*u.ampere, places=3)
        self.assertAlmostEqual(self.eng5.current(), 78.182*u.ampere, places=3)
        self.assertAlmostEqual(self.eng6.current(), 42.542*u.ampere, places=3)
        self.assertAlmostEqual(self.eng7.current(), 55.455*u.ampere, places=3)

        self.assertAlmostEqual(
            self.ccm1.charge_current(), 103.177*u.ampere, places=3)
        self.assertAlmostEqual(
            self.ccm2.charge_current(), 117.685*u.ampere, places=3)
        self.assertAlmostEqual(
            self.qdtl.charge_current(), 97.996*u.ampere, places=3)

    def test_by_amperage(self):
        current = self.ccm2.charge_current()
        section = self.ccm2_section.by_amperage(current)
        self.assertEqual(section, 50*u.millimeter**2)

    def test_by_voltage_drop(self):
        current = self.ccm2.charge_current()
        distance = 29*u.meter
        max_fall = 0.03
        section = self.ccm2_section.by_voltage_drop(
            current, distance, max_fall)
        self.assertEqual(section, 25*u.millimeter**2)

    def test_by_short_circuit(self):
        max_current = 5*u.kiloampere
        time = 0.01*u.second
        section = self.ccm2_section.by_short_circuit(max_current, time)
        self.assertEqual(section, 6*u.millimeter**2)

    def test_protection_condutor(self):
        current = self.ccm2.charge_current()
        distance = 29*u.meter
        max_fall = 0.03
        max_current = 5*u.kiloampere
        time = 0.01*u.second

        amperage_section = self.ccm2_section.by_amperage(current)
        voltage_drop_section = self.ccm2_section.by_voltage_drop(
            current, distance, max_fall)
        short_circuit_section = (
            self.ccm2_section.by_short_circuit(max_current, time)
        )

        phase_section = (
            max(amperage_section, voltage_drop_section, short_circuit_section)
        )

        condutor_section = self.ccm2_section.protection_condutor(phase_section)
        self.assertEqual(condutor_section, 25*u.millimeter**2)

    def test_power_factor(self):
        total = self.ccm1.power + self.ccm2.power + self.qdtl.power
        reactive_power = total.inductive_power_factor_to(0.92)

        self.assertAlmostEqual(
            total.power_factor,
            0.73,
            places=2
        )

        self.assertAlmostEqual(
            reactive_power,
            -57.185*u.kilovolt_ampere_reactive,
            places=3
        )
