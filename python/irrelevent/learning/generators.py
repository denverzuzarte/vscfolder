# how to use generators

def generator():
    for x in range (1,8,2):
        yield ('hello',str(x));

#fibonacci using generators

def fibo():
    while True:
        yield a;
        yield b;
        a=a+b;
        b=b+a;
for x in fibo():
    print (x);
    if x>13:
        quit();

