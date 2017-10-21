import pytest
from fourth import *

def test_percentageOf():
    assert percentageOf(1000, 10) == 100

def test_fundsAtTheEndOfYear():
    assert fundsAtTheEndOfYear(10000, 10, 15, []) == 1000
    assert fundsAtTheEndOfYear(10000, 10, 15, [1000]) == 1000 + 1000 * 1.15

def test_nestEggFixed():
    assert nestEggFixed(10000, 10, 15, 5) == [1000.0, 2150, 3472.5, 4993.375, 6742.38125]
    # defensive programming
    with pytest.raises(AssertionError) as excinfo:
        nestEggFixed(-1, 10, 15, 5)
    excinfo.match('Salary must be greater than or equal to zero')
    with pytest.raises(AssertionError) as excinfo:
        nestEggFixed(1, -1, 15, 5)
    excinfo.match('Save must be a percentage between 0 and 100')
    with pytest.raises(AssertionError) as excinfo:
        nestEggFixed(1, 101, 15, 5)
    excinfo.match('Save must be a percentage between 0 and 100')
    with pytest.raises(AssertionError) as excinfo:
        nestEggFixed(1, 1, -1, 5)
    excinfo.match('Growth rate must be a percentage between 0 and 100')
    with pytest.raises(AssertionError) as excinfo:
        nestEggFixed(1, 1, 101, 5)
    excinfo.match('Growth rate must be a percentage between 0 and 100')
    with pytest.raises(AssertionError) as excinfo:
        nestEggFixed(1, 1, 1, -1)
    excinfo.match('Years must be a value between 0 and 100')

def test_nestEggVariable():
    assert nestEggVariable(10000, 10, [3, 4, 5, 0, 3]) == [1000.0, 2040.0, 3142.0, 4142.0, 5266.26]

def test_postRetirement():
    assert postRetirement(100000, [10, 5, 0, 5, 1], 30000) == [80000.000000000015, 54000.000000000015, 24000.000000000015, -4799.9999999999854, -34847.999999999985]

def near(value, to, epsilon = 0.1):
    return abs(value - to) <= epsilon

def test_maxExpensesFor():
    assert near(maxExpensesFor(1000, [0], 0.1), 1000)

def test_findMaxExpenses():
    assert near(findMaxExpenses(10000, 10, [2, 3, 5, 0, 3], [10, 5, 0, 5, 1], .01), 1227.4)
