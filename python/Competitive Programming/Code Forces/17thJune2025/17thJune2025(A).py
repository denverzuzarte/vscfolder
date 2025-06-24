k=int(input())
ans=[]
for a in range (0,k):
    arr=[]
    n, s = map(int, input().split())
    arr = list(map(int, input().split()))
    mini=arr[0]
    maxi=arr[n-1]
    diff=min(s-mini,maxi-s)
    if diff<=0:
        ans.append(max(s-mini,maxi-s))
    else:
        ans.append(maxi-mini+diff)
for b in range (0,k):
    print(ans[b])