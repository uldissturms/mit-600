from eighth import *
from time import *
import pytest

subjects = loadSubjects('subjects.txt')
test_subjects = {
    's1': (1, 1),
    's2': (2, 1),
    's3': (3, 3),
    's4': (4, 4),
    's5': (5, 5),
    's6': (20, 10),
    's7': (24, 12),
    's8': (20, 15),
    's10': (20, 20),
    's1.1': (1, 10),
    's1.2': (1, 20),
    's1.3': (1, 30)
}

def test_parse():
    parsed = parse('subject1,7,14')
    assert parsed[0] == 'subject1'
    assert parsed[1][0] == 7
    assert parsed[1][1] == 14

def test_load_subjects():
    assert loadSubjects('subjects.txt')['2.00'] == (5,9)

def test_greedy_advisor_by_value():
    assert greedyAdvisor(test_subjects, 5, cmpValue) == {'s5': (5, 5)}
    assert greedyAdvisor(subjects, 8, cmpValue) == {'7.17': (10, 1), '7.18': (10, 2), '7.19': (10, 5)}

def test_greedy_advisor_by_work():
    assert greedyAdvisor(test_subjects, 5, cmpWork) == {'s1': (1, 1), 's2': (2, 1), 's3': (3, 3)}

def test_greedy_advisor_by_ratio():
    assert greedyAdvisor(test_subjects, 5, cmpRatio) == {'s1': (1, 1), 's2': (2, 1), 's3': (3, 3)}

# Problem 3: Subject Selection By Brute Force
# O(2^n) - where n = number of subjects
# By changing max work we affect how many times brute force will execute branch that adds current subject (subset.append(i) & recurse)
def test_brute_force_time():
    start = clock()
    bruteForceAdvisor(subjects, 7)
    assert clock() - start < 6

def test_dynamic_programming_advisor():
    assert dpAdvisor(test_subjects, 4) == {'s2': (2, 1), 's3': (3, 3)}
    assert dpAdvisor(subjects, 4) == {'12.04': (7, 1), '6.00': (10, 1), '15.01': (7, 1), '7.17': (10, 1)}
    assert dpAdvisor(subjects, 30) == {
        '10.18': (10, 3),
        '12.04': (7, 1),
        '12.09': (8, 2),
        '14.02': (10, 2),
        '15.01': (7, 1),
        '18.08': (10, 3),
        '2.03': (6, 1),
        '22.01': (6, 2),
        '22.03': (10, 2),
        '22.06': (10, 3),
        '24.12': (6, 1),
        '6.00': (10, 1),
        '7.00': (7, 1),
        '7.05': (8, 2),
        '7.06': (4, 1),
        '7.16': (7, 1),
        '7.17': (10, 1),
        '7.18': (10, 2)
    }

# Problem 5 Observations
# pseudo-polynominal time, dynamic programming can calculate result for 2000 max work while brute force can only 7. Optimisation lies in the fact that sub-problems are overlapping and we can re-use best known solutionsin similar situations, especially when there is no more available work
def test_dynamic_programming_advisor_time():
    start = clock()
    dpAdvisor(subjects, 2000)
    assert clock() - start < 6
