# string and string searching

from string import *
from problem import *

problem("write two functions, called countSubStringMatch and countSubStringMatchRecursive that take two arguments, a key string and a target string.")

def countSubStringMatch(target, key):
    count = 0
    offset = 0
    match = find(target, key)
    while (match != -1 and offset <= len(target)):
        count += 1
        offset = match + (1 if key == "" else len(key))
        match = find(target, key, offset)
    return count

def countSubStringMatchRecursive(target, key, count = 0):
    match = find(target, key)
    if (match == -1):
        return count
    if (target == ""):
        return count + 1
    return countSubStringMatchRecursive(target[(match + 1):], key, count + 1)

problem("return all matches")

def subStringMatchExact(target, key, offset = 0, matches = []):
    match = find(target, key)
    if (match == -1):
        return matches
    if (target == ""):
        return append(offset + match, matches)
    return subStringMatchExact(
        target[(match + 1):],
        key,
        offset + match + 1,
        append(offset + match, matches)
    )

problem("return partial matches")

def constrainedMatchPair(firstMatch, secondMatch, lenght):
    return [x for x in firstMatch if x + lenght + 1 in secondMatch]

# NOTE: changed signature from the one provided in course to match other functions in this module
def subStringMatchOneSub(target, key):
    allAnswers = []
    for miss in range(0,len(key)):
        # miss picks location for missing element
        # key1 and key2 are substrings to match
        key1 = key[:miss]
        key2 = key[miss+1:]
        # match1 and match2 are tuples of locations of start of matches
        # for each substring in target
        match1 = subStringMatchExact(target,key1)
        match2 = subStringMatchExact(target,key2)
        # when we get here, we have two tuples of start points
        # need to filter pairs to decide which are correct
        filtered = constrainedMatchPair(match1,match2,len(key1))
        allAnswers = allAnswers + filtered
    return list(set(allAnswers))

problem("matches with exactly one substitution")

def filterExactlyOneSub(matches, target, key):
    return [m for m in matches if target[m:(m + len(key))] != key]

def subStringMatchExactlyOneSub(target, key):
    return filterExactlyOneSub(
        subStringMatchOneSub(target, key),
        target,
        key)
