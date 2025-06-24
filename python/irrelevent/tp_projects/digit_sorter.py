print('Enter number');
n=0;
n1=len(n);
x=0;count=[0,0,0,0,0,0,0,0,0,0];
arr=[];
while x<n1:
    arr.append(int(n[x]));
    x=x+1;
def dig_count(dig):
    co=0;
    for b in arr:
        if b==dig:
            co=co+1;
    return co;
x=0
while x<10:
    count[x]=dig_count(x);
    x=x+1;
def maxi(count):
    x=0;k=0;max=0;
    while x<10:
        if max<=count[x]:
            max=count[x];
            k=x;
        x=x+1;
    return k,max;
x=0;
while x<10:
    s,m=maxi(count);
    j=0;
    while j<m:
        print(s,end='');
        j=j+1;
    count[s]=0;
    x=x+1;