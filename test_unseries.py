import pytest
from uncertainties import ufloat
from unseries import Series


@pytest.fixture()
def zero():
    """
    Returns zero series
    """
    return Series(1)


def test_zero_input(zero):
    assert [str(zero), zero.pprint(), "{}".format(zero)] == ['0'] * 3


def test__eq(zero):
    # TODO: implement `__eq__` via properly implemented `__repr__`
    assert Series(1) == zero


def test__add_simple():
    z1 = Series(2, {0: ufloat(1, 0.3), 1: ufloat(2, .003)})
    z2 = Series(2, {0: ufloat(-1, 0.4), 1: ufloat(-2, .004)})
    z3 = Series(2, {0: ufloat(0, 0.5), 1: ufloat(0, .005)})
    z12 = z1 + z2
    assert z12 == z3


def test__add():
    z1 = Series(2, {0: ufloat(1, 0.3), 1: ufloat(2, .003)})
    z2 = Series(3, {0: ufloat(-1, 0.4), 1: ufloat(-2, .004), 2: ufloat(999, .1)})
    z3 = Series(2, {0: ufloat(0, 0.5), 1: ufloat(0, .005)})
    assert z1 + z2 == z3


def test__radd():
    assert False


def test__sub():
    assert False


def test__mul():
    assert False


def test__rmul():
    assert False


def test__neg():
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


def test_coeffs():
    assert False


def test_pprint():
    assert False


def test__str():
    assert False


def test_subs():
    assert False


def test_save():
    assert False
