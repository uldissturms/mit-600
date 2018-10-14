from algorithms import *
from generate import *
from peak import *

to_str = lambda x: str(x)

def diagnose (data, problem, alg, peak):
    is_peak = problem.isPeak(peak)
    if not is_peak:
        print('Problem: \n{}'.format(format(data)))
        print('{}: {}, NOT peak'.format(alg, peak))


def format (problem):
    return ''.join(['[' + ','.join(map(to_str, row)) + '],\n' for row in problem])

def test():
    data = randomProblem(10, 10)
    problem = createProblem(data)
    diagnose(data, problem, 'A1', algorithm1(problem))
    diagnose(data, problem, 'A2', algorithm2(problem))
    diagnose(data, problem, 'A3', algorithm3(problem))
    diagnose(data, problem, 'A4', algorithm4(problem))

for i in range(0, 10000):
    test()
