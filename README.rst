unseries
########


.. image:: https://travis-ci.org/kirienko/unseries.svg?branch=master
:target: https://travis-ci.org/kirienko/unseries


This package allows to deal with power series which coefficients contain uncertainties.


It is build on top of ``uncertainties`` python package (see `here <https://pypi.python.org/pypi/uncertainties>`_).

Scope
-----
For now the following fuctions are available:
    - series addition and subtraction
    - comparision (*greater than*, *less than*)
    - series multiplication
    - series inversion, i.e. ``Z(g) ➝ 1/Z(g)``
    - series division (in the assumption that all powers are non-negative)
    - exponentiation
    - analitic differentiation
    - substitution, i.e. calculation of a series ``Z(g)`` at the point ``g₀`` to a number with uncertainty
    - approximation
    - some technical functions: ``pprint``, ``save`` [to file],

Example
-------
Assume two series:

``Z₁(g) =  1.00(30) +  2.0000(30) g``

``Z₂(g) = -1.0(4) - 2.000(4) g + 999.00(10) g²``

Then
``Z₁+Z₂ = 0.0(5) + 0.000(5) g + 999.00(10) g²``


.. code-block:: python

    from unseries import Series
    z1 = Series(2, {0: ufloat(1, 0.3), 1: ufloat(2, .003)})
    z2 = Series(3, {0: ufloat(-1, 0.4), 1: ufloat(-2, .004), 2: ufloat(999, .1)})
    print z1 + z2