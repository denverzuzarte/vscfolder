import random
import math
n=int(input('enter the strength - '));
i=1;e=1;
while i<=n:
    a=math.pow(e,1+1/10**n)
    if (a/e-1)<1/10**n:
        e=e+1/10**i
    else:
        e=e-1/10**i;
        i=i+1;
print(e);