import math
n=3;
primes2=[2];
primes=[2];
while n<10000:
    factors=True;
    for x in primes2:
        if n%x==0:
            factors=False;
            break;
    if factors:
        primes.append(n);
        primes2=[h for h in primes if h<=n**0.5];
    n=n+1;
print(primes);