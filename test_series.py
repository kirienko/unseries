from unittest import TestCase

from uncertainties import ufloat

from uncertSeries import Series


class TestSeries(TestCase):
    #     def test_diff(self):
    #         self.fail()
    #
    #     def test__approx(self):
    #         self.fail()
    #
    #     def test_coeffs(self):
    #         self.fail()
    #
    #     def test_pprint(self):
    #         self.fail()
    #
    #     def test_subs(self):
    #         self.fail()
    #
    #     def test_save(self):
    #         self.fail()

    def test__add(self):
        z1 = Series(2, {0: ufloat(1, 0.3), 1: ufloat(2, .003)})
        z2 = Series(3, {0: ufloat(-1, 0.4), 1: ufloat(-2, .004), 2: ufloat(999, .1)})
        z3 = Series(2, {0: ufloat(0, 0.5), 1: ufloat(0, .005)})
        # FIXME
        # self.assertEqual(z1 + z2, z3)
