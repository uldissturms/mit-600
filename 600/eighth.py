# 6.00 Problem Set 8
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

import time
from itertools import *
from functools import *

SUBJECT_FILENAME = "subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def parse(line):
    subject, value, effort = line.strip().split(',')
    return (subject, (int(value), int(effort)))

def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """
    inputFile = open(filename)
    return dict([parse(line) for line in inputFile])

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print(res)

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    return  val1 - val2

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return  work2 - work1

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return int((float(val1) / work1) - (float(val2) / work2))

#
# Problem 2: Subject Selection By Greedy Optimization
#

def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    ranked = sorted(subjects.items(), key=cmp_to_key(comparator), reverse=True)
    workAvailable = maxWork
    selected = []
    for subject in ranked: # can return early if workAvailable == 0
        subject_value = subject[1]
        if workAvailable >= subject_value[WORK]:
            workAvailable -= subject_value[WORK]
            selected.append(subject)

    return dict(selected)

def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    nameList = subjects.keys()
    tupleList = subjects.values()
    bestSubset, bestSubsetValue = \
            bruteForceAdvisorHelper(tupleList, maxWork, 0, None, None, [], 0, 0)
    outputSubjects = {}
    for i in bestSubset:
        outputSubjects[nameList[i]] = tupleList[i]
    return outputSubjects

def bruteForceAdvisorHelper(subjects, maxWork, i, bestSubset, bestSubsetValue,
                            subset, subsetValue, subsetWork):
    # Hit the end of the list.
    if i >= len(subjects):
        if bestSubset == None or subsetValue > bestSubsetValue:
            # Found a new best.
            return subset[:], subsetValue
        else:
            # Keep the current best.
            return bestSubset, bestSubsetValue
    else:
        s = subjects[i]
        # Try including subjects[i] in the current working subset.
        if subsetWork + s[WORK] <= maxWork:
            subset.append(i)
            bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                    maxWork, i+1, bestSubset, bestSubsetValue, subset,
                    subsetValue + s[VALUE], subsetWork + s[WORK])
            subset.pop()
        bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                maxWork, i+1, bestSubset, bestSubsetValue, subset,
                subsetValue, subsetWork)
        return bestSubset, bestSubsetValue

# Problem 4: Subject Selection By Dynamic Programming
#
def append(list, item):
    new_list = list[:]
    new_list.append(item)
    return new_list

def dpAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work) that contains a
    set of subjects that provides the maximum value without exceeding maxWork.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    items = sorted(subjects.items()) # so that we get deterministic results when testing - not really needed, could be injected from tests
    result, _ = smart_advisor(items, len(items) - 1, maxWork)
    return dict(result)

def cache_and_return(key, value, cache):
    cache[key] = value
    return value

def smart_advisor(items, index, workAvailable, cache={}):
    if (index, workAvailable) in cache:
        return cache[(index, workAvailable)]

    subject = items[index]
    subject_name = subject[0]
    subject_value = subject[1]
    key = (index, workAvailable)

    if index == 0:
        if subject_value[WORK] <= workAvailable:
            return cache_and_return(key, ([subject], subject_value[VALUE]), cache)
        return cache_and_return(key, ([], 0), cache)

    if subject_value[WORK] > workAvailable:
        return cache_and_return(key, smart_advisor(items, index - 1, workAvailable, cache), cache)

    no_selection, no_value = smart_advisor(items, index - 1, workAvailable, cache)
    yes_selection, yes_value = smart_advisor(items, index - 1, workAvailable - subject_value[WORK], cache)
    yes_value += subject_value[VALUE]
    yes_selection = append(yes_selection, subject)

    return cache_and_return(
        key,
        (no_selection, no_value) if no_value >= yes_value else (yes_selection, yes_value),
        cache
    )
