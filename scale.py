# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
from fractions import Fraction
import math

c = '1'
d = '9/8'
e = '5/4'
f = '4/3'
g = '3/2'
a = '5/3'

c_hi = '2'

cg = [c, g]
ceg = [c, e, g]
fac = [f, a, c_hi]
maj_penta = [c, d, e, g, a]  # d/a = 27/40
cegfa = [c, e, f, g, a]  # e/f = 15/16
freq = [Fraction(x) for x in cegfa]

max_cycle = 1
max_r = 0
min_r = 1
for i in range(len(freq)):
    for j in range(i + 1, len(freq)):
        r = freq[i]/freq[j]
        max_r = max(r, max_r)
        min_r = min(r, min_r)
        cycle = r.numerator*r.denominator
        if cycle > max_cycle:
            max_cycle = cycle
            print(freq[i], freq[j], r)
            
print(max_cycle, max_r, min_r)
