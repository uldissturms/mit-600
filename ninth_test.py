from ninth import *
from os import linesep

def test_triangle_are():
    assert Triangle(3, 8).area() == 12

def shape_set_with(shapes):
    shapeSet = ShapeSet()
    for s in shapes:
        shapeSet.addShape(s)
    return shapeSet

def test_cmp_shapes():
    assert cmp_shapes(Square(2), Square(2)) == 0
    assert cmp_shapes(Square(1), Square(2)) == -1
    assert cmp_shapes(Square(1), Circle(2)) == 1
    assert cmp_shapes(Square(2), Triangle(1, 1)) == -1

def test_shape_set_add():
    assert str(shape_set_with([Circle(2)])) == 'Circle with radius 2.0'
    assert str(shape_set_with([
        Triangle(1, 1),
        Square(4),
        Circle(2),
        Square(1)
        ])) == 'Circle with radius 2.0{0}Square with side 1.0{0}Square with side 4.0{0}Triangle with base 1.0 and height 1.0'.format(linesep)

def test_find_largest():
    expected = Circle(4)
    shapes = [
        expected,
        Triangle(1.2, 2.5),
        Square(3.6),
        Triangle(1.6, 6.4),
        Circle(2.2)
    ]
    assert findLargest(shape_set_with(shapes)) == [expected]

def test_find_multiple_largest():
    expectedOne = Triangle(3, 8)
    expectedTwo = Triangle(4, 6)
    shapes = [
        Circle(0.2),
        expectedOne,
        expectedTwo
    ]
    largest = findLargest(shape_set_with(shapes))
    assert len(largest) == 2
    assert expectedOne in largest
    assert expectedTwo in largest

def test_shape_from_params():
    assert shapeFromParams(['circle', 3]) == Circle(3)

def test_read_shapes_from_file():
    shapes = readShapesFromFile('shapes.txt')
    assert len(list(shapes)) == 16
    assert Circle(2) in shapes
    assert Triangle(3, 6.6) in shapes
