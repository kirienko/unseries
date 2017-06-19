# encoding: utf8

from sympy import Add
from uncertainties import __version_info__ as uncert_version
from uncertainties import ufloat, ufloat_fromstr
from uncertainties.core import Variable, AffineScalarFunc

if uncert_version < (3, 0):
    raise Warning("Your version of uncertanties is not supported. Try\n$ sudo pip install uncertainties --upgrade")


class Series:
    """
    The class that provides the expansion in powers of g up to the n-th order, taking the error into account.
    """

    def __init__(self, n, d={0: 0}, name='g', analytic=False):
        self.n = n
        self.gSeries = d
        self.name = name
        self.analytic = analytic
        for k, v in d.items():
            if isinstance(v, AffineScalarFunc):
                self.gSeries[k] = v
            elif isinstance(v, (list, tuple)):
                self.gSeries[k] = ufloat(v[0], v[1])
            elif isinstance(v, str):
                self.gSeries[k] = ufloat_fromstr(v)
            elif isinstance(v, int):
                self.gSeries[k] = v
                self.analytic = True
            else:
                print("Series constructor warning: Type(v)={}".format(type(v)))  # TODO: raise error
        for i in range(0, n):
            if i not in d.keys():
                if self.analytic:
                    self.gSeries[i] = 0
                else:
                    self.gSeries[i] = ufloat(0, 0)

    def __lt__(self, other):
        return len(self.gSeries) < len(other.gSeries)

    def __add__(self, other):
        tmp = dict(self.gSeries)
        # print "From __add__:",self.analytic," + ",other.pprint() ## FIXME
        if isinstance(other, Series):
            stop = min(self.n, other.n)
            if stop == 0:
                stop = max(self.n, other.n)
            for g in other.gSeries.keys():
                if g <= stop:
                    try:
                        tmp[g] += other.gSeries[g]
                    except KeyError:
                        tmp[g] = other.gSeries[g]
        elif isinstance(other, (int, float)):
            tmp[0] += other
        else:
            print("{} {}".format(type(self), type(other)))
            raise NotImplementedError
        return Series(len(tmp), tmp, name=self.name, analytic=self.analytic)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-1) * other

    def __mul__(self, other):
        tmp = {}
        if isinstance(other, Series):
            stop = min(self.n, other.n)
            for i in self.gSeries.keys():
                for j in other.gSeries.keys():
                    if (i + j) <= stop:
                        try:
                            tmp[i + j] += self.gSeries[i] * other.gSeries[j]
                        except  KeyError:
                            tmp[i + j] = self.gSeries[i] * other.gSeries[j]
            res = Series(max(self.n, other.n), tmp, name=self.name, analytic=self.analytic)
        elif isinstance(other, (int, float, Variable, AffineScalarFunc, Add)):
            for i in self.gSeries.keys():
                tmp[i] = self.gSeries[i] * other
            res = Series(self.n, tmp, name=self.name, analytic=self.analytic)
        elif other == 0 or sum(map(lambda v: v == 0, self.gSeries.values())) == len(self.gSeries):
            return 0
        # elif isinstance(other, sympy.core.add.Add):
        #     print "\n\nself=",self
        #     print "other=",other
        #     return 0
        else:
            print("\nself = {}, type(self) = {}".format(self.gSeries, type(self)))
            print("\nother = {}, type(other) = {}".format(other, type(other)))
            raise NotImplementedError
        return res

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        return self * (-1)

    def __invert__(self):
        """ Z.__invert__() = 1/Z
        1/(1+x)=Sum_i (-1)^i x^i
        """
        res = Series(self.n, {}, self.name, analytic=self.analytic)
        if self.gSeries[0] == 1:
            c = 1.
            normed_series = self + Series(self.n, {0: -1}, self.name, analytic=self.analytic)  # <-- it's -1!
        elif self.gSeries[0] != 0:
            c = 1. / self.gSeries[0]
            normed_series = self / self.gSeries[0] + Series(self.n, {0: -1}, self.name,
                                                            analytic=self.analytic)  # <-- it's -1!
        else:
            raise NotImplementedError("no constant term in series: %s" % self.gSeries)
        # if self.gSeries[0] == 1:
        #    tmp = Series(self.gSeries[1:], n = self.n-1, name=self.name)
        #        for i in range(tmp.n):
        for i in range(len(self.gSeries)):
            res += (-1) ** i * normed_series ** i
        return res * c

    def __div__(self, other):
        """ For now we assume all the powers of g as non-negative
        """
        if isinstance(other, Series):
            return self * other.__invert__()
        elif isinstance(other, (int, float, Variable, AffineScalarFunc)):
            return self * (1. / other)
        else:
            raise NotImplementedError("type: {}; {}".format(type(other), other.__repr__()))

    def __rdiv__(self, other):
        return other * self.__invert__()

    def __pow__(self, power, modulo=None):
        if isinstance(power, int) and power > 1:
            return reduce(lambda x, y: x * y, [self] * power)
        elif isinstance(power, int) and power == 1:
            return self
        elif isinstance(power, int) and power == 0:
            if self.analytic:
                return Series(self.n, {0: 1}, self.name, analytic=self.analytic)
            else:
                return Series(self.n, {0: ufloat(1, 0)}, self.name, analytic=self.analytic)
        else:
            print("power = {}, type(power) = {}".format(power, type(power)))
            raise NotImplementedError

    def diff(self):
        """
        Differentiation of the polynomial in g
        """
        res = {}
        for i in range(len(self.gSeries) - 1):
            res[i] = (i + 1) * self.gSeries[i + 1]
        return Series(self.n, res, analytic=self.analytic)

    def __repr__(self):
        return self.pprint()

    ## FIXME
    def _approx(self, other):
        for k, v in self.gSeries.items():
            if v != other.gSeries[k]:
                return False
        return True

    def __str__(self):
        """
        The result is truncated according to the error, indicating the accuracy of the least significant digit
        """
        res = ''
        for g, c in self.gSeries.items():
            if c != 0 and g == 0 and isinstance(c, int):
                res += " %d + " % (c)
            elif c != 0 and g == 0:
                res += " %s + " % (c.format('S'))
            elif c != 0 and g <= self.n and isinstance(c, (Variable, AffineScalarFunc)):
                if c.s < 1e-14:
                    res += "%s * %s**%s + " % (str(c.n), self.name, str(g))
                else:
                    res += " %s * %s**%s + " % (c.format('S'), self.name, str(g))
            elif c != 0 and g <= self.n and isinstance(c, (int, float)):
                res += "%s * %s**%s + " % (str(c), self.name, str(g))
        return res[:-2] or '0'

    def coeffs(self):
        """

        """
        return map(lambda x: float(x.format('S').split("(")[0]), self.gSeries.values())[:self.n + 1]

    def pprint(self):
        res = ""
        for g, c in self.gSeries.items():
            if c != 0 and g <= self.n and not self.analytic:
                res += "(%s ± %s) * %s**%s + " % (str(c.n), str(c.s), self.name, str(g))
            elif c != 0 and g <= self.n and self.analytic:
                try:
                    this_term = c.format('S')
                except AttributeError:
                    this_term = str(c)
                res += "(%s) * %s**%s + " % (this_term, self.name, str(g))
        return res[:-2] or '0'

    def __len__(self):
        return len(self.gSeries)

    def subs(self, point):
        res = Series(n=self.n, d={0: ufloat(0, 0)}, name=point.name, analytic=self.analytic)
        for i, c in self.gSeries.items():
            res += c * (point ** i)
        return res

    def save(self):
        """Save value to file"""
        slov = ''
        for k, v in self.gSeries.items():
            slov += "%d: '%s', " % (k, v)
        print("Series({}, {}, '{}')".format(self.n, slov, self.name))


if __name__ == "__main__":
    Z1 = Series(1)
    Z2 = Series(2, {0: ufloat(-4, 0.3), 1: ufloat(2, .002)})
    print("Z1 = {}".format(Z1))
    print("Z2 = {}".format(Z2))
    print("Z2.diff() = {}".format(Z2.diff()))
    print("Z2 - Z2 = {}".format(Z2-Z2))
    print("1/Z2 = {}".format(1 / Z2))
    print("Z1*Z2 = {}".format(Z1 * Z2))
    print("Z2**2 = {}".format(Z2 ** 2))
