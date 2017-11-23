# This file implements some very rudimentary matrix-like and vector-like operations
# It is used by the tester.
# You are welcome to use these functions for the lab implementation as well,
# though this isn't expected to be necessary.

import random
import operator
import math

try:
    all([])
except NameError:
    # The all() function was introduced in Python 2.5.
    # Provide our own implementation if it's not available here.
    def all(iterable):
        for element in iterable:
            if not element:
                return False
        return True


def unit_vector(vec1, vec2):
    """ Return a unit vector pointing from vec1 to vec2 """
    diff_vector = list(map(operator.sub, vec2, vec1))
    
    scale_factor = math.sqrt( sum( [x**2 for x in diff_vector] ) )
    if scale_factor == 0:
        scale_factor = 1 # We don't have an actual vector, it has zero length
    return [x/scale_factor for x in diff_vector]

def vector_compare(vec1, vec2, delta):
    """ Compare two vectors
    Confirm that no two corresponding fields differ by more than delta """
    return all( map(lambda x,y: (abs(x-y) < delta), vec1, vec2) )
    
def validate_euclidean_distance(list1, list2, dist):
    """
    Confirm that the given distance is the Euclidean distance
    between list1 and list2 by establishing a unit vector between
    the two lists and seeing if vec * dist + list1 == list2
    """

    vec = unit_vector(list1, list2)
    target = list(map(lambda jmp, base: jmp * dist + base, vec, list1))
    return vector_compare(target, list2, 0.01)

def random_list(length):
    return [ random.randint(1,100) for x in range(length) ]
