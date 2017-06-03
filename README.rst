unseries
########


.. image:: https://travis-ci.org/kirienko/unseries.svg?branch=master
:target: https://travis-ci.org/kirienko/unseries


This package allows to deal with power series which coefficients contain uncertainties.


It is build on top of ``uncertainties`` python package (see `here <https://pypi.python.org/pypi/uncertainties>`_).


Example
-------
Assume two series:

``Z₁(g) =  1.00(30) +  2.0000(30) g``

``Z₂(g) = -1.0(4) - 2.000(4)*g + 999.00(10) g²``

Then
``Z₁+Z₂ = 0.0(5) + 0.000(5) g + 999.00(10) g²``


.. code-block:: python

    from unseries import Series
    z1 = Series(2, {0: ufloat(1, 0.3), 1: ufloat(2, .003)})
    z2 = Series(3, {0: ufloat(-1, 0.4), 1: ufloat(-2, .004), 2: ufloat(999, .1)})
    print z1 + z2