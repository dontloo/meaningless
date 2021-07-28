# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
from fractions import Fraction
import math

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

c = '1'
e = '5/4'
f = '4/3'
g = '3/2'
a = '5/3'

c_hi = '2'

cg = [c, g]
ceg = [c, e, g]
fac = [f, a, c_hi]
freq = [Fraction(x) for x in cg]

max_cycle = 1
for x in freq:
    for y in freq:
        r = x/y
        cycle = r.numerator*r.denominator
        if cycle > max_cycle:
            max_cycle = cycle
            print(x, y, r, lcm(x,y))
            
print(max_cycle)
