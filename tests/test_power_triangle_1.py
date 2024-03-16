import unittest
import instelec as ie
u = ie.ureg


class TestPowerTriangle(unittest.TestCase):
    def setUp(self):
        self.triangle = ie.PowerTriangle(60*u.kilovolt_ampere, 0.9)

    def test_apparent(self):
        self.assertAlmostEqual(
            self.triangle.apparent,
            60*u.kilovolt_ampere,
            places=3
        )

    def test_active(self):
        self.assertAlmostEqual(
            self.triangle.active,
            54*u.kilowatt,
            places=3
        )

    def test_reactive(self):
        self.assertAlmostEqual(
            self.triangle.reactive,
            26.153*u.kilovolt_ampere_reactive,
            places=3
        )

    def test_power_factor(self):
        self.assertAlmostEqual(self.triangle.power_factor, 0.9, places=3)

    def test_power_factor_to(self):
        inf, sup = self.triangle.power_factor_to(0.92)

        self.assertAlmostEqual(
            inf, -49.157*u.kilovolt_ampere_reactive, places=3)

        self.assertAlmostEqual(
            sup, -3.149*u.kilovolt_ampere_reactive, places=3)
