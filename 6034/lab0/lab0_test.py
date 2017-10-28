from lab0 import *

def test_product_with_one():
     assert Product([1, 2]).simplify() == Product([2])

def test_nested_product():
     assert Product([2, Product([3, 4])]).simplify() == Product([2, 3, 4])

def test_product_with_nested_sum():
     assert Product([2, Sum([3, 4])]).simplify() == Sum([Product([2, 3]), Product([2, 4])])

def test_complex_sum():
    simplified = Sum([2, Product([3, Product([8, Sum([3, 12]), 5])])]).simplify()
    assert simplified == Sum([2,
        Product([5, 3, 8, 3]),
        Product([5, 3, 8, 12])
    ])
