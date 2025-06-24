import random
n=int(input('enter the strength - '));
i=0;count=0;
while i<10**n:
    x=random.random();
    y=random.random();
    if (x**2+y**2)<=1 :
        count =count+1;
    i=i+1;
print (4*count/(10**n));