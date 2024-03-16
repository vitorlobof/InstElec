import unittest
import instelec as ie
u = ie.ureg


class TestCondutorDimensioning(unittest.TestCase):
    def setUp(self):
        self.eng1 = ie.Engine(ie.PowerTriangle(8*u.kilovolt_ampere, 0.8), 1)
        self.eng2 = ie.Engine(ie.PowerTriangle(35*u.kilovolt_ampere, 0.7), 3)
        self.eng3 = ie.Engine(ie.PowerTriangle(11*u.kilovolt_ampere, 0.8), 1)

        self.eng4 = ie.Engine(ie.PowerTriangle(26*u.kilovolt_ampere, 0.7), 3)
        self.eng5 = ie.Engine(ie.PowerTriangle(11*u.kilovolt_ampere, 0.8), 1)
        self.eng6 = ie.Engine(ie.PowerTriangle(17.2*u.kilovolt_ampere, 0.7), 1)

        self.eng7 = ie.Engine(ie.PowerTriangle(8*u.kilovolt_ampere, 0.8), 1)
        self.eng8 = ie.Engine(ie.PowerTriangle(28*u.kilovolt_ampere, 0.7), 3)
        self.eng9 = ie.Engine(ie.PowerTriangle(12.2*u.kilovolt_ampere, 0.8), 1)

        self.ccm1 = ie.EngineGroup({self.eng1: 1, self.eng2: 1, self.eng3: 1})
        self.ccm2 = ie.EngineGroup({self.eng4: 1, self.eng5: 1, self.eng6: 1})
        self.qdtl = ie.EngineGroup({self.eng7: 1, self.eng8: 1, self.eng9: 1})

        self.eng1_section = ie.CupperPVC(
            "B1", self.eng1.power.power_factor, self.eng1.phase_num)
        self.eng2_section = ie.CupperPVC(
            "B1", self.eng2.power.power_factor, self.eng2.phase_num)
        self.eng3_section = ie.CupperPVC(
            "B1", self.eng3.power.power_factor, self.eng3.phase_num)
        self.eng4_section = ie.CupperPVC(
            "B1", self.eng4.power.power_factor, self.eng4.phase_num)
        self.eng5_section = ie.CupperPVC(
            "B1", self.eng5.power.power_factor, self.eng5.phase_num)
        self.eng6_section = ie.CupperPVC(
            "B1", self.eng6.power.power_factor, self.eng6.phase_num)
        self.eng7_section = ie.CupperPVC(
            "B1", self.eng7.power.power_factor, self.eng7.phase_num)
        self.eng8_section = ie.CupperPVC(
            "B1", self.eng8.power.power_factor, self.eng8.phase_num)
        self.eng9_section = ie.CupperPVC(
            "B1", self.eng9.power.power_factor, self.eng9.phase_num)

        self.ccm1_section = ie.CupperPVC(
            "B1", self.ccm1.power.power_factor, self.eng1.phase_num)
        self.ccm2_section = ie.CupperPVC(
            "B1", self.ccm2.power.power_factor, self.eng1.phase_num)
        self.qdtl_section = ie.CupperPVC(
            "B1", self.qdtl.power.power_factor, self.eng1.phase_num)

        self.ccm1_section.grouping_correction(3)
        self.ccm2_section.grouping_correction(3)
        self.qdtl_section.grouping_correction(3)

    def test_apparent_power(self):
        self.assertAlmostEqual(self.eng1.power.apparent,
                               8*u.kilovolt_ampere, places=2)
        self.assertAlmostEqual(self.eng2.power.apparent,
                               35*u.kilovolt_ampere, places=2)
        self.assertAlmostEqual(self.eng3.power.apparent,
                               11*u.kilovolt_ampere, places=2)
        self.assertAlmostEqual(self.eng4.power.apparent,
                               26*u.kilovolt_ampere, places=2)
        self.assertAlmostEqual(self.eng5.power.apparent,
                               11*u.kilovolt_ampere, places=2)
        self.assertAlmostEqual(self.eng6.power.apparent,
                               17.2*u.kilovolt_ampere, places=2)
        self.assertAlmostEqual(self.eng7.power.apparent,
                               8*u.kilovolt_ampere, places=2)
        self.assertAlmostEqual(self.eng8.power.apparent,
                               28*u.kilovolt_ampere, places=2)
        self.assertAlmostEqual(self.eng9.power.apparent,
                               12.2*u.kilovolt_ampere, places=2)

        self.assertAlmostEqual(self.ccm1.power.apparent,
                               53.86*u.kilovolt_ampere, places=2)
        self.assertAlmostEqual(self.ccm2.power.apparent,
                               54.1*u.kilovolt_ampere, places=2)
        self.assertAlmostEqual(self.qdtl.power.apparent,
                               48.06*u.kilovolt_ampere, places=2)

    def test_active_power(self):
        self.assertAlmostEqual(self.eng1.power.active,
                               6.4*u.kilowatt, places=2)
        self.assertAlmostEqual(self.eng2.power.active,
                               24.5*u.kilowatt, places=2)
        self.assertAlmostEqual(self.eng3.power.active,
                               8.8*u.kilowatt, places=2)
        self.assertAlmostEqual(self.eng4.power.active,
                               18.2*u.kilowatt, places=2)
        self.assertAlmostEqual(self.eng5.power.active,
                               8.8*u.kilowatt, places=2)
        self.assertAlmostEqual(self.eng6.power.active,
                               12.04*u.kilowatt, places=2)
        self.assertAlmostEqual(self.eng7.power.active,
                               6.4*u.kilowatt, places=2)
        self.assertAlmostEqual(self.eng8.power.active,
                               19.6*u.kilowatt, places=2)
        self.assertAlmostEqual(self.eng9.power.active,
                               9.76*u.kilowatt, places=2)

        self.assertAlmostEqual(self.ccm1.power.active,
                               39.70*u.kilowatt, places=2)
        self.assertAlmostEqual(self.ccm2.power.active,
                               39.04*u.kilowatt, places=2)
        self.assertAlmostEqual(self.qdtl.power.active,
                               35.76*u.kilowatt, places=2)

    def test_reactive_power(self):
        self.assertAlmostEqual(self.eng1.power.reactive,
                               4.8*u.kilovolt_ampere_reactive, places=2)
        self.assertAlmostEqual(self.eng2.power.reactive,
                               24.99*u.kilovolt_ampere_reactive, places=2)
        self.assertAlmostEqual(self.eng3.power.reactive,
                               6.6*u.kilovolt_ampere_reactive, places=2)
        self.assertAlmostEqual(self.eng4.power.reactive,
                               18.57*u.kilovolt_ampere_reactive, places=2)
        self.assertAlmostEqual(self.eng5.power.reactive,
                               6.6*u.kilovolt_ampere_reactive, places=2)
        self.assertAlmostEqual(self.eng6.power.reactive,
                               12.28*u.kilovolt_ampere_reactive, places=2)
        self.assertAlmostEqual(self.eng7.power.reactive,
                               4.8*u.kilovolt_ampere_reactive, places=2)
        self.assertAlmostEqual(self.eng8.power.reactive,
                               20*u.kilovolt_ampere_reactive, places=2)
        self.assertAlmostEqual(self.eng9.power.reactive,
                               7.32*u.kilovolt_ampere_reactive, places=2)

        self.assertAlmostEqual(self.ccm1.power.reactive,
                               36.39*u.kilovolt_ampere_reactive, places=2)
        self.assertAlmostEqual(self.ccm2.power.reactive,
                               37.45*u.kilovolt_ampere_reactive, places=2)
        self.assertAlmostEqual(self.qdtl.power.reactive,
                               32.12*u.kilovolt_ampere_reactive, places=2)

    def test_currents(self):
        self.assertAlmostEqual(self.eng1.current(), 36.36*u.ampere, places=2)
        self.assertAlmostEqual(self.eng2.current(), 53.18*u.ampere, places=2)
        self.assertAlmostEqual(self.eng3.current(), 50*u.ampere, places=2)

        self.assertAlmostEqual(self.eng4.current(), 39.5*u.ampere, places=2)
        self.assertAlmostEqual(self.eng5.current(), 50*u.ampere, places=2)
        self.assertAlmostEqual(self.eng6.current(), 78.18*u.ampere, places=2)

        self.assertAlmostEqual(self.eng7.current(), 36.36*u.ampere, places=2)
        self.assertAlmostEqual(self.eng8.current(), 42.54*u.ampere, places=2)
        self.assertAlmostEqual(self.eng9.current(), 55.45*u.ampere, places=2)

        self.assertAlmostEqual(self.ccm1.charge_current(),
                               103.18*u.ampere, places=2)
        self.assertAlmostEqual(self.ccm2.charge_current(),
                               117.68*u.ampere, places=2)
        self.assertAlmostEqual(
            self.qdtl.charge_current(), 98*u.ampere, places=2)

    def test_nominal_currents(self):
        self.assertEqual(self.eng1_section.nominal_current(
            self.eng1_section.by_amperage(self.eng1.current())), 41*u.ampere)
        self.assertEqual(self.eng2_section.nominal_current(
            self.eng2_section.by_amperage(self.eng2.current())), 68*u.ampere)
        self.assertEqual(self.eng3_section.nominal_current(
            self.eng3_section.by_amperage(self.eng3.current())), 57*u.ampere)

        self.assertEqual(self.eng4_section.nominal_current(
            self.eng4_section.by_amperage(self.eng4.current())), 50*u.ampere)
        self.assertEqual(self.eng5_section.nominal_current(
            self.eng5_section.by_amperage(self.eng5.current())), 57*u.ampere)
        self.assertEqual(self.eng6_section.nominal_current(
            self.eng6_section.by_amperage(self.eng6.current())), 101*u.ampere)

        self.assertEqual(self.eng7_section.nominal_current(
            self.eng7_section.by_amperage(self.eng7.current())), 41*u.ampere)
        self.assertEqual(self.eng8_section.nominal_current(
            self.eng8_section.by_amperage(self.eng8.current())), 50*u.ampere)
        self.assertEqual(self.eng9_section.nominal_current(
            self.eng9_section.by_amperage(self.eng9.current())), 57*u.ampere)

        # self.assertEqual(self.ccm1_section.nominal_current(
        #     self.ccm1_section.by_amperage(self.ccm1.charge_current())), 175*u.ampere)
        # self.assertEqual(self.ccm2_section.nominal_current(
        #     self.ccm2_section.by_amperage(self.ccm2.charge_current())), 175*u.ampere)
        # self.assertEqual(self.qdtl_section.nominal_current(
        #     self.qdtl_section.by_amperage(self.qdtl.charge_current())), 144*u.ampere)

    def test_section_of_eng1(self):
        current = self.eng1.current()
        distance = 29*u.meter
        max_fall = 0.03
        max_current = 4*u.kiloampere
        time = 0.01*u.second

        amperage_section = self.eng1_section.by_amperage(current)
        voltage_drop_section = self.eng1_section.by_voltage_drop(
            current, distance, max_fall)
        short_circuit_section = self.eng1_section.by_short_circuit(
            max_current, time)

        self.assertEqual(amperage_section, 6*u.millimeter**2)
        self.assertEqual(voltage_drop_section, 6*u.millimeter**2)
        self.assertEqual(short_circuit_section, 4*u.millimeter**2)

        phase_section = max(
            amperage_section, voltage_drop_section, short_circuit_section)

        protection_section = self.eng1_section.protection_condutor(
            phase_section)

        self.assertEqual(phase_section, 6*u.millimeter**2)
        self.assertEqual(protection_section, 6*u.millimeter**2)

    def test_section_of_eng2(self):
        current = self.eng2.current()
        distance = 29*u.meter
        max_fall = 0.03
        max_current = 4*u.kiloampere
        time = 0.01*u.second

        amperage_section = self.eng2_section.by_amperage(current)
        voltage_drop_section = self.eng2_section.by_voltage_drop(
            current, distance, max_fall)
        short_circuit_section = self.eng2_section.by_short_circuit(
            max_current, time)

        self.assertEqual(amperage_section, 16*u.millimeter**2)
        self.assertEqual(voltage_drop_section, 6*u.millimeter**2)
        self.assertEqual(short_circuit_section, 4*u.millimeter**2)

        phase_section = max(
            amperage_section, voltage_drop_section, short_circuit_section)

        protection_section = self.eng2_section.protection_condutor(
            phase_section)

        self.assertEqual(phase_section, 16*u.millimeter**2)
        self.assertEqual(protection_section, 16*u.millimeter**2)

    def test_section_of_eng3(self):
        current = self.eng3.current()
        distance = 29*u.meter
        max_fall = 0.03
        max_current = 4*u.kiloampere
        time = 0.01*u.second

        amperage_section = self.eng3_section.by_amperage(current)
        voltage_drop_section = self.eng3_section.by_voltage_drop(
            current, distance, max_fall)
        short_circuit_section = self.eng3_section.by_short_circuit(
            max_current, time)

        self.assertEqual(amperage_section, 10*u.millimeter**2)
        self.assertEqual(voltage_drop_section, 10*u.millimeter**2)
        self.assertEqual(short_circuit_section, 4*u.millimeter**2)

        phase_section = max(
            amperage_section, voltage_drop_section, short_circuit_section)

        protection_section = self.eng3_section.protection_condutor(
            phase_section)

        self.assertEqual(phase_section, 10*u.millimeter**2)
        self.assertEqual(protection_section, 10*u.millimeter**2)
    
    def test_section_of_ccm1(self):
        current = self.ccm1.charge_current()
        distance = 160*u.meter
        max_fall = 0.03
        max_current = 4*u.kiloampere
        time = 0.01*u.second

        amperage_section = self.ccm1_section.by_amperage(current)
        voltage_drop_section = self.ccm1_section.by_voltage_drop(
            current, distance, max_fall)
        short_circuit_section = self.ccm1_section.by_short_circuit(
            max_current, time)

        self.assertEqual(amperage_section, 50*u.millimeter**2)
        self.assertEqual(voltage_drop_section, 70*u.millimeter**2)
        self.assertEqual(short_circuit_section, 4*u.millimeter**2)

        phase_section = max(
            amperage_section, voltage_drop_section, short_circuit_section)

        protection_section = self.ccm1_section.protection_condutor(
            phase_section)

        self.assertEqual(phase_section, 70*u.millimeter**2)
        self.assertEqual(protection_section, 35*u.millimeter**2)

    def test_power_factor(self):
        total_power = self.ccm1.power + self.ccm2.power + self.qdtl.power

        self.assertAlmostEqual(self.ccm1.power.power_factor, 0.74, places=2)
        self.assertAlmostEqual(self.ccm2.power.power_factor, 0.72, places=2)
        self.assertAlmostEqual(self.qdtl.power.power_factor, 0.74, places=2)
        self.assertAlmostEqual(total_power.power_factor, 0.73, places=2)

        self.assertAlmostEqual(
            total_power.inductive_power_factor_to(0.92),
            -57.19*u.kilovolt_ampere_reactive,
            places=2
        )
