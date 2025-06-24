x=0;fibonachi=1;hidden=0;
n=input('how many terms');
while x<int(n):
    x=x+1;
    print(fibonachi);
    fibonachi=fibonachi+hidden;
    hidden=fibonachi-hidden;