# encoding: utf8
import pytest
from uncertainties import ufloat
from unseries import Series


@pytest.fixture()
def zero():
    """
    Returns zero series
    """
    return Series(1)


@pytest.fixture()
def one_two_three():
    """
    Analytic series: z(g) = 1 + 2g² + 3g⁴
    """
    return Series(4, {0: 1, 1: 2, 4: 3})


@pytest.fixture()
def z1():
    return Series(2, {0: ufloat(1, 0.3), 1: ufloat(2, .003)})


@pytest.fixture()
def z2():
    return Series(2, {0: ufloat(-1, 0.4), 1: ufloat(-2, .004)})


def test_zero_input(zero):
    assert [str(zero), zero.pprint(), "{}".format(zero)] == ['0'] * 3


def test__eq(zero):
    # TODO: implement `__eq__` via properly implemented `__repr__`
    assert str(Series(1)) == str(zero)


def test__neg(zero, z1, z2):
    assert str(zero) == str(-zero)
    assert str(z1) == str(-(-z1))
    assert str(z2) == str(-(-z2))


def test__add_simple(z1, z2):
    z3 = Series(2, {0: ufloat(0, 0.5), 1: ufloat(0, .005)})
    z12 = z1 + z2
    assert str(z12) == str(z3)


def test__add():
    z1 = Series(2, {0: ufloat(1, 0.3), 1: ufloat(2, .003)})
    z2 = Series(3, {0: ufloat(-1, 0.4), 1: ufloat(-2, .004), 2: ufloat(999, .1)})
    z3 = Series(2, {0: ufloat(0, 0.5), 1: ufloat(0, .005)})
    assert z1 + z2 == z3


def test__radd(z1, z2):
    z12 = z1
    z12 += z2
    z21 = z2 + z1
    assert str(z12) == str(z21)


def test__sub():
    assert False


def test__mul():
    assert False


def test__rmul():
    assert False


def test__invert():
    assert False


def test__div():
    assert False


def test__rdiv():
    assert False


def test__pow():
    assert False


def test_diff():
    assert False


def test__approx():
    assert False


def test_coeffs_z1(z1):
    assert z1.coeffs() == [1, 2]


def test_coeffs_z3():
    z3 = Series(4, {0: ufloat(-1, 0.4), 1: ufloat(-2, .004), 3: ufloat(999, .1)})
    assert z3.coeffs() == [-1, -2, 0, 999]


def test_coeffs_z4():
    z4 = Series(5, {0: ufloat(-1, 0.4), 1: ufloat(-2, .004), 3: ufloat(999, .1)})
    assert z4.coeffs() == [-1, -2, 0, 999, 0]


def test_pprint(z1, one_two_three):
    # FIXME: UTF8 support
    # print(z1)
    # assert z1.pprint == "(1.0 ± 0.3) * g**0 + (2.0 ± 0.003) * g**1"
    # TODO: remove redundant parentheses
    assert one_two_three.pprint() == "(1) * g**0 + (2) * g**1 + (3) * g**4"


def test__str():
    assert False


def test_subs():
    assert False


def test_save():
    assert False
