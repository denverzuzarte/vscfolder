x=0;
n=int(input('help - '));
arr=[];
while x<n:
    y=0;
    arr.append([]);
    while y<2*n+1:
        arr[x].append(0);
        y=y+1;
    x=x+1;
arr[0][n]=1;
x=1
while x<n:
    y=1;
    while y<2*n:
        arr[x][y]=arr[x-1][y-1]+arr[x-1][y+1];
        y=y+1;
    x=x+1;
x=0;
while x<n:
    y=0;
    print('');
    while y<2*n+1:
        if arr[x][y]==0:
            print('   ',end='');
        else:
            print(arr[x][y],end='');
        y=y+1;
    x=x+1;