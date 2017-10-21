from third import *

def test_countSubStringMatch():
    assert countSubStringMatch("abc", "abc") == 1
    assert countSubStringMatch("aba", "a") == 2
    assert countSubStringMatch("abcabc", "abc") == 2
    assert countSubStringMatch("abcdabc", "abc") == 2
    assert countSubStringMatch("abc", "def") == 0
    assert countSubStringMatch("abc", "") == 4

def test_countSubStringMatchRecursive():
    assert countSubStringMatchRecursive("abc", "abc") == 1
    assert countSubStringMatchRecursive("aba", "a") == 2
    assert countSubStringMatchRecursive("abcabc", "abc") == 2
    assert countSubStringMatchRecursive("abcdabc", "abc") == 2
    assert countSubStringMatchRecursive("abc", "def") == 0
    assert countSubStringMatchRecursive("abc", "") == 4

def test_subStringMatchExact():
    assert subStringMatchExact("abc", "abc") == [0]
    assert subStringMatchExact("aba", "a") == [0, 2]
    assert subStringMatchExact("abcabc", "abc") == [0, 3]
    assert subStringMatchExact("abc", "def") == []
    assert subStringMatchExact("abc", "") == [0, 1, 2, 3]

def test_contrainedMatchPair():
    assert constrainedMatchPair([0, 3, 5, 9], [7], 1) == [5]
    assert constrainedMatchPair([0, 3, 5, 9], [7, 11], 1) == [5, 9]
    assert constrainedMatchPair([1], [4], 1) == []

def test_subStringMatchExactlyOneSub():
    assert subStringMatchExactlyOneSub("abcdef", "ab1") == [0]
    assert subStringMatchExactlyOneSub("abcdefabd", "ab1") == [0, 6]
    assert subStringMatchExactlyOneSub("abcdef", "abc") == []
    assert subStringMatchExactlyOneSub("abc", "b") == [0, 2]
    assert subStringMatchExactlyOneSub("abc", "") == []
