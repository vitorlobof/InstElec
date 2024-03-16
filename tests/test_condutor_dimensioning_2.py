import unittest
import instelec as ie
u = ie.ureg


class TestCondutorDimensioning(unittest.TestCase):
    def setUp(self):
        self.eng1 = ie.Engine(ie.PowerTriangle(8*u.kilovolt_ampere, 0.8), 1)
        self.eng2 = ie.Engine(ie.PowerTriangle(35*u.kilovolt_ampere, 0.7), 3)
        self.eng3 = ie.Engine(ie.PowerTriangle(11*u.kilovolt_ampere, 0.8), 1)

        self.group = ie.EngineGroup({
            self.eng1: 1,
            self.eng2: 1,
            self.eng3: 1
        })

        self.eng1_section = ie.CupperPVC(
            "B1",
            self.eng1.power.power_factor,
            self.eng1.phase_num
        )

        self.eng2_section = ie.CupperPVC(
            "B1",
            self.eng2.power.power_factor,
            self.eng2.phase_num
        )

        self.eng3_section = ie.CupperPVC(
            "B1",
            self.eng3.power.power_factor,
            self.eng3.phase_num
        )

        self.group_section = ie.CupperPVC(
            'B1',
            self.group.power.power_factor,
            self.group.phase_num
        )

    def test_apparent_power(self):
        self.assertAlmostEqual(self.eng1.power.apparent,
                               8*u.kilovolt_ampere, places=2)
        self.assertAlmostEqual(self.eng2.power.apparent,
                               35*u.kilovolt_ampere, places=2)
        self.assertAlmostEqual(self.eng3.power.apparent,
                               11*u.kilovolt_ampere, places=2)

    def test_active_power(self):
        self.assertAlmostEqual(self.eng1.power.active,
                               6.4*u.kilowatt, places=2)
        self.assertAlmostEqual(self.eng2.power.active,
                               24.5*u.kilowatt, places=2)
        self.assertAlmostEqual(self.eng3.power.active,
                               8.8*u.kilowatt, places=2)

    def test_reactive_power(self):
        self.assertAlmostEqual(self.eng1.power.reactive,
                               4.8*u.kilovolt_ampere_reactive, places=2)
        self.assertAlmostEqual(self.eng2.power.reactive,
                               24.99*u.kilovolt_ampere_reactive, places=2)
        self.assertAlmostEqual(self.eng3.power.reactive,
                               6.6*u.kilovolt_ampere_reactive, places=2)

    def test_currents(self):
        self.assertAlmostEqual(self.eng1.current(), 36.36*u.ampere, places=2)
        self.assertAlmostEqual(self.eng2.current(), 53.18*u.ampere, places=2)
        self.assertAlmostEqual(self.eng3.current(), 50.00*u.ampere, places=2)

        self.assertAlmostEqual(
            self.group.charge_current(),
            103.18*u.ampere, places=2
        )

    def test_nominal_currents(self):
        self.assertEqual(self.eng1_section.nominal_current(self.eng1_section.by_amperage(self.eng1.current())), 41*u.ampere)
        self.assertEqual(self.eng2_section.nominal_current(self.eng2_section.by_amperage(self.eng2.current())), 68*u.ampere)
        self.assertEqual(self.eng3_section.nominal_current(self.eng3_section.by_amperage(self.eng3.current())), 57*u.ampere)

    def test_by_amperage(self):
        current = self.eng1.current()
        section = self.eng1_section.by_amperage(current)
        self.assertEqual(section, 6*u.millimeter**2)

        current = self.eng2.current()
        section = self.eng2_section.by_amperage(current)
        self.assertEqual(section, 16*u.millimeter**2)

        current = self.eng3.current()
        section = self.eng3_section.by_amperage(current)
        self.assertEqual(section, 10*u.millimeter**2)

    def test_by_voltage_drop(self):
        distance = 29*u.meter
        max_fall = 0.03

        current = self.eng1.current()
        section = self.eng1_section.by_voltage_drop(
            current, distance, max_fall)
        self.assertEqual(section, 6*u.millimeter**2)

        current = self.eng2.current()
        section = self.eng2_section.by_voltage_drop(
            current, distance, max_fall)
        self.assertEqual(section, 6*u.millimeter**2)

        current = self.eng3.current()
        section = self.eng3_section.by_voltage_drop(
            current, distance, max_fall)
        self.assertEqual(section, 10*u.millimeter**2)

    def test_by_short_circuit(self):
        max_current = 5*u.kiloampere
        time = 0.01*u.second

        section = self.eng1_section.by_short_circuit(max_current, time)
        self.assertEqual(section, 6*u.millimeter**2)

        section = self.eng2_section.by_short_circuit(max_current, time)
        self.assertEqual(section, 6*u.millimeter**2)

        section = self.eng3_section.by_short_circuit(max_current, time)
        self.assertEqual(section, 6*u.millimeter**2)

    # def test_protection_condutor(self):
    #     current = self.group.charge_current()
    #     distance = 29*u.meter
    #     max_fall = 0.03
    #     max_current = 5*u.kiloampere
    #     time = 0.01*u.second

    #     amperage_section = self.ccm2_section.by_amperage(current)
    #     voltage_drop_section = self.ccm2_section.by_voltage_drop(
    #         current, distance, max_fall)
    #     short_circuit_section = (
    #         self.ccm2_section.by_short_circuit(max_current, time)
    #     )

    #     phase_section = (
    #         max(amperage_section, voltage_drop_section, short_circuit_section)
    #     )

    #     condutor_section = self.ccm2_section.protection_condutor(phase_section)
    #     self.assertEqual(condutor_section, 35*u.millimeter**2)

    def test_power_factor(self):
        self.assertAlmostEqual(
            self.group.power.power_factor,
            0.74,
            places=2
        )

        self.assertAlmostEqual(
            self.group.power.inductive_power_factor_to(0.92),
            -19.48*u.kilovolt_ampere_reactive,
            places=2
        )
