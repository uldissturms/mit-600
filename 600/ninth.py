# 6.00 Problem Set 9
#
# Name:
# Collaborators:
# Time:

from string import *
from os import linesep

class Shape(object):
    def area(self):
        raise AttributeException("Subclasses should override this method.")

class Square(Shape):
    def __init__(self, h):
        """
        h: length of side of the square
        """
        self.side = float(h)
    def area(self):
        """
        Returns area of the square
        """
        return self.side**2
    def __str__(self):
        return 'Square with side ' + str(self.side)
    def __eq__(self, other):
        """
        Two squares are equal if they have the same dimension.
        other: object to check for equality
        """
        return type(other) == Square and self.side == other.side
    def __hash__(self):
        return id(self)

class Circle(Shape):
    def __init__(self, radius):
        """
        radius: radius of the circle
        """
        self.radius = float(radius)
    def area(self):
        """
        Returns approximate area of the circle
        """
        return 3.14159*(self.radius**2)
    def __str__(self):
        return 'Circle with radius ' + str(self.radius)
    def __eq__(self, other):
        """
        Two circles are equal if they have the same radius.
        other: object to check for equality
        """
        return type(other) == Circle and self.radius == other.radius
    def __hash__(self):
        return id(self)

#
# Problem 1: Create the Triangle class
#
class Triangle(Shape):
    def __init__(self, base, height):
        self.base = float(base)
        self.height = float(height)
    def area(self):
        return (self.base * self.height) / 2
    def __str__(self):
        return 'Triangle with base {0} and height {1}'.format(self.base, self.height)
    def __eq__(self, other):
        return type(other) == Triangle and self.base == other.base and self.height == other.height
    def __hash__(self):
        return id(self)

#
# Problem 2: Create the ShapeSet class
#
## TO DO: Fill in the following code skeleton according to the
##    specifications.

def cmp(a, b):
    return (a > b) - (a < b)

def cmp_shapes(left, right):
    leftType = type(left)
    rightType = type(right)
    if leftType == rightType:
        return cmp(left.area(), right.area())
    return cmp(str(leftType), str(rightType))

class ShapeSet:
    def __init__(self):
        self.shapes = set()
    def addShape(self, sh):
        self.shapes.add(sh)
    def __iter__(self):
        return iter(sorted(self.shapes)) # deterministic sorting
    def __str__(self):
        return linesep.join([str(s) for s in sorted(self.shapes, cmp=cmp_shapes)])
    def __getitem__(self, key):
        return list(self.shapes)[key]
#
# Problem 3: Find the largest shapes in a ShapeSet
#
def findLargest(shapes):
    """
    Returns a tuple containing the elements of ShapeSet with the
       largest area.
    shapes: ShapeSet
    """
    largestSet = None
    largest = 0
    for s in shapes:
        if (s.area() > largest):
            largestSet = []
            largest = s.area()
        if (s.area() == largest):
            largestSet.append(s)
    return largestSet

#
# Problem 4: Read shapes from a file into a ShapeSet
#
def shapeFromParams(params):
    return globals()[params[0].capitalize()](*params[1:])

def readShapesFromFile(filename):
    """
    Retrieves shape information from the given file.
    Creates and returns a ShapeSet with the shapes found.
    filename: string
    """
    shapeSet = ShapeSet()
    inputFile = open(filename)
    for line in inputFile:
        params = line.rstrip(linesep).split(',')
        shapeSet.addShape(shapeFromParams(params))
    return shapeSet
