def ice_baby(arrmin,arrmax): # Takes in the arrays
    # find biggest array that takes in values
    a = sorted(arrmin, reverse=True)
    b = sorted(arrmax, reverse=True)
    i=0;
    prob_a=0
    for goodboi in a:
        if goodboi>b[i]:
            prob_a+=1
        i=i+1
    i=0;
    prob_b=0
    for goodboi in b:
        if goodboi>a[i]:
            prob_b+=1
        i=i+1
    if (prob_b>=prob_a and prob_b>0):
        badpair=arrmax.index(b[0])
        arrmax.pop(badpair)
        arrmin.pop(badpair)
        ice_baby(arrmin,arrmax)
    if (prob_a>=prob_b and prob_a>0):
        badpair=arrmin.index(a[0])
        arrmax.pop(badpair)
        arrmin.pop(badpair)
        ice_baby(arrmin,arrmax)
    else:
        return len(arrmax)

if __name__ == "__main__":
    k=int(input())
    ans=[]
    for a in range (0,k):
        ans.append([])
        n=int(input())
        l=[]
        r=[]
        for u in range (0,n):
            h, j = map(int, input().split())
            l.append(h)
            r.append(j)
            ans[a].append(ice_baby(l,r))
    for b in range (0,k):
        print(ans[b])