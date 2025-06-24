import math
x=0;g=1;arr=[[]];
n=8#int(input('what is your number of rows'));
'''
while x < n:
    k=0;j=0;
    while j<=(n-x):
        print(" ",end='');
        j=j+1;
    while k < x:
        
        print(g," ",end='');
        k=k+1;
    x=x+1;
    print("");
'''
j=0
while j<n:
    x=0
    arr.append([]);
    if j==0:
        while x<(2*n+1):
            arr[j].append(0);
            x=x+1;
            if x==n+1:
                arr[0][n]=1;
    else:
        while x<(2*n+1):
            x=x+1;
            arr[j].append(0);
    j=j+1;
i=1;
while i<n:
    j=1;
    while j<n*2:
        arr[i][j]=(arr[i-1][j-1])+(arr[i-1][j+1]);
        j=j+1;
    i=i+1;
while i<n:
    j=1;
    while j<n*2:
        if arr[i][j]==0:
            arr[i][j]=" ";
        j=j+1;
    i=i+1;
import pandas as pd