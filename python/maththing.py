import random
from sympy import *

def getnum():
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
                                

ans = {}

n = 0
for a, b, c, d, e, f, g in getnum():
    n += 1
    x = symbols('x')
    eq1 = Eq((a/b)*((c*x)+d)+(e*x), (f*x)+g)
    try:
        solv, *_ = solveset(eq1, x).args
        solv = float(solv)
    except:
        pass
    solv = round(solv, 2)
    print(f"{n} - {str(solv).ljust(5)} {a} {b} {c} {d} {e} {f} {g}", end="\r")
    ans[solv] = [a, b, c, d, e, f, g]
    

print("All answers calculated...")
ans = dict(sorted(ans.items(), key=lambda x: x[0], reverse=True))
print("Sorted answers...")

with open("mathsort.txt", "w") as file:
    for x, (a, b, c, d, e, f, g) in ans.items():
        
        dist = f"{a} {b} {c} {d} {e} {f} {g}"
        print(f"{dist.rjust(20)} - {x}")
        file.write(f"{str(x).ljust(6)} - {a} {b} {c} {d} {e} {f} {g}")
    