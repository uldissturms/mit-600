# time complexity - O(i)
def fact0(i):
    assert type(i) == int and i >= 0
    if i == 0 or i == 1:
        return 1
    return i * fact0(i-1)
'''
fact0(5)
5 * fact0(4)
5 * 4 * fact(3)
5 * 4 * 3 * fact(2)
5 * 4 * 3 * 2 * fact(1)
5 * 4 * 3 * 2 * 1
'''

# time complexity - O(i)
def fact1(i):
    assert type(i) == int and i >= 0
    res = 1
    while i > 1:
        res = res * i
        i -= 1
    return res
'''
fact1(5)
1 * 5
5 * 4
20 * 3
60 * 2
120
'''

# time complexity - O(s^2)
def makeSet(s):
    assert type(s) == str
    res = ''
    for c in s: # O(s)
        if not c in res: # O(s)
            res = res + c
    return res
'''
makeSet('stuffs')
s = 'stuffs'
res    | c |
-------|---|
's'    | s |
'st'   | t |
'stu'  | u |
'stuf' | f |
'stuf' | f |
'stuf' | s |
'''

# time complexity - O(s1*s2)
def intersect(s1, s2):
    assert type(s1) == str and type(s2) == str
    s1 = makeSet(s1) # O(s1)
    s2 = makeSet(s2) # O(s2)
    res = ''
    for e in s1: # O(s1)
        if e in s2: # O(s2)
            res = res + e
    return res
'''
intersect('stuff', 'must')
s1 = 'stuf', s2 = 'must' # O(s1 + s2)
res | e |
----| - |
s   | s |
st  | t |
stu | u |
stu | f |
'''

def swap0(s1, s2):
    assert type(s1) == list and type(s2) == list
    tmp = s1[:] # O(s1)
    s1 = s2[:] # O(s2)
    s2 = tmp
    return

s1 = [1]
s2 = [2]
swap0(s1, s2)
print s1, s2
'''
swap0(s1, s2)
tmp = [1]
s1 = [2] # local
s2 = [1] # local
[1] [2] # print s1, s2
'''

def swap1(s1, s2):
    assert type(s1) == list and type(s2) == list
    return s2, s1

s1 = [1]
s2 = [2]
s1, s2 = swap1(s1, s2)
print s1, s2
'''
swap1(s1, s2)
[2] [1] # print s1, s2
'''

def rev(s):
    assert type(s) == list
    for i in range(len(s)/2):
        tmp = s[i]
        s[i] = s[-(i+1)]
        s[-(i+1)] = tmp

s = [1,2,3]
rev(s)
print s
'''
rev(s)
 i | tmp |  s        |
---|-----|-----------|
 0 | 1   | [3, 2, 1] |
 1 | 2   | [3, 2, 1] |
'''
