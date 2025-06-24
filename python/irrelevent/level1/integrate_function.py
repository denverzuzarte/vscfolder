import math
import functions
#we are gonna integrate functions across the x axis
a=float(input('enter the start value - '));
b=float(input('enter the end value - '));
def func(x):
    return functions.function(x); # enter the function you wanna integrate
I=0
delta=(b-a)/1000000;
if a<b:
    x=a
    while x<b-delta:
        I=I+func(x)*delta;
        x=x+delta;
elif b<a:
    x=b;
    while x<a-delta:
        I=I-func(x)*delta;
        x=x+delta;
print(4*I);