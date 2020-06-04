import sys
import unittest
from collections import deque

from dnaseqlib import RollingHash, compareSequences

# Utility classes #

# Maps integer keys to a set of arbitrary values.


class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.d = {}
        for k, v in pairs:
            self.put(k, v)

    # Associates the value v with the key k.

    def put(self, k, v):
        self.d.setdefault(k, []).append(v)
    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.

    def get(self, k):
        return self.d.get(k, [])

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)


def subsequenceHashes(seq, k):
    w = deque()
    i = 0

    for s in seq:
        w.append(s)
        if i == k - 1:
            rh = RollingHash(w)
            yield (rh.current_hash(), (0, list(w)))
        elif i >= k:
            rh.slide(w.popleft(), s)
            if len(w) < k:
                return
            yield (rh.current_hash(), (i - k + 1, list(w)))

        i += 1


# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)


def intervalSubsequenceHashes(seq, k, m):
    w = deque()
    i = 0
    l = m

    for s in seq:
        w.append(s)
        if i == k - 1:
            rh = RollingHash(w)
            yield (rh.current_hash(), (0, list(w)))
        elif i >= k:
            rh.slide(w.popleft(), s)
            if len(w) < k:
                return
            l -= 1
            if l == 0:
                l = m
                yield (rh.current_hash(), (i - k + 1, list(w)))

        i += 1


class TestDNASeq(unittest.TestCase):
    def test_subseq_hashes(self):
        self.assertListEqual(
            list(subsequenceHashes(['A', 'T', 'A', 'T'], 2)),
            [
                (539, (0, ['A', 'T'])),
                (653, (1, ['T', 'A'])),
                (539, (2, ['A', 'T'])),
            ]
        )

    def test_subseq_hashes_interval(self):
        self.assertListEqual(
            list(intervalSubsequenceHashes(['A', 'T', 'A', 'T', 'T', 'T'], 2, 2)),
            [
                (539, (0, ['A', 'T'])),
                (539, (2, ['A', 'T'])),
                (672, (4, ['T', 'T'])),
            ]
        )

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).


def getExactSubmatches(a, b, k, m):
    ah = intervalSubsequenceHashes(a, k, m)
    d = Multidict(ah)
    for k, (bI, bS) in subsequenceHashes(b, k):
        for (aI, aS) in d.get(k):
            if bS == aS:
                yield (aI, bI)


# if __name__ == '__main__':
#     unittest.main()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: {0} [file_a.fa] [file_b.fa] [output.png]".format(sys.argv[0]))
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500, 500), sys.argv[1], sys.argv[2], 8, 100)
