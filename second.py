# 6a + 9b + 20c = n // nugget problem

def problem(name):
    print "Problem: " + name
    return

def maxFor(nuggets, weight):
    return (nuggets / weight) + 1

def combination(a, b, c, expected):
    if (a * aWeigth + b * bWeight + c * cWeight == expected):
        output(a, b, c, expected)

def output(a, b, c, expected):
    print "a: {0}, b: {1}, c: {2} makes: {3}".format(a, b, c, expected)
    return

def can_be_bought(quantity, packages):
    for a in range(0, maxFor(quantity, packages[0])):
        for b in range(0, maxFor(quantity, packages[1])):
            for c in range(0, maxFor(quantity, packages[2])):
                if (a * packages[0] + b * packages[1] + c * packages[2] == quantity):
                    return True
    return False

problem("it is possible to buy 50, 51, 52, 53, 54 and 55 nuggets")

maxNuggets = 55
aWeigth = 6
bWeight = 9
cWeight = 20

for a in range(0, maxFor(maxNuggets, aWeigth)):
    for b in range(0, maxFor(maxNuggets, bWeight)):
        for c in range(0, maxFor(maxNuggets, cWeight)):
            combination(a, b, c, 50)
            combination(a, b, c, 51)
            combination(a, b, c, 52)
            combination(a, b, c, 53)
            combination(a, b, c, 54)
            combination(a, b, c, 55)

problem("show how, given solution to 50-55, one can derive solutions to 56-65")

print "50 + 6 makes: 56"
print "51 + 6 makes: 57"
print "52 + 6 makes: 58"
print "53 + 6 makes: 59"
print "54 + 6 makes: 60"
print "55 + 6 makes: 61"
print "53 + 9 makes: 62"
print "54 + 9 makes: 63"
print "55 + 9 makes: 64"
print "50 + 9 + 6  makes: 65"

problem("if it's possible to buy x, x + 1,..., x + 5 sets of nugets for some x, then it's possible to buy any number of nugets >=x, given the nugets come in 6, 9 and 20 packs")

print "x, x + 1, ..., x + 5,"
print "# x + 6, (x + 1) + 6 = x + 7, ..., (x + 5) + 6 = x + 11," # adding a pack of 6
print "(x + 3) + 9 = x + 12, (x + 4) + 9 = x + 13, (x + 5) + 9 = x + 14," # adding a pack of 9
print "x + 6 + 9 = x + 15, (x + 1) + 6 + 9 = x + 16, ..., (x + 5) + 6 + 9 = x + 20" # adding a pack of 6 and 9
print "x + 20, (x + 1) + 20 = x + 21, ..."
print "having x .. x + 21 as source any number can be constructed by adding a 6 or 9 or 20 to a number from source, indeed having x .. x + 5, it's enought to have packs of 6 and 9 to be able to construct any number"

from collections import deque

def find_largest_nugets(packages):
    minimum = min(packages)
    queue = deque([], minimum)
    largest = 0
    for n in range(minimum, 200):
        if can_be_bought(n, packages):
            queue.append(n)
            if list(queue) == range(queue[0], queue[0] + minimum):
                return largest
        else:
            largest = n
    return n

packages = [6, 9, 20]

print "largest number of nugets that cannot be bought for {0} in exact quantity is: {1}".format(packages, find_largest_nugets(packages))
