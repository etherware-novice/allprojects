import random
from sympy import *

def gennum():
    for a in range(1, 10):
        for b in range(1, 10):
            if b == a: continue
            for c in range(1, 10):
                if c in (a, b): continue
                for d in range(1, 10):
                    if d in (a, b, c): continue
                    for e in range(1, 10):
                        if e in (a, b, c, d): continue
                        for f in range(1, 10):
                            if f in (a, b, c, d, e): continue
                            for g in range(1, 10):
                                if g in (a, b, c, d, e, f): continue
                                yield (a, b, c, d, e, f, g)


for a, b, c, d, e, f, g in getnum():

    solv = solveset(Eq((a/b)(cx+d)+ex, fx+g), x)
    print(solve)
    input()
