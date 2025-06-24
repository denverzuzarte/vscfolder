import random
def genshin(a,b):
    if (b==0):
        return True
    if (a==0 and b==1):
        return False
    if (b==1 and a==1):
        return True
i=0
n=1000000
prob=0
arr=[0]
while i<n :
    ran=random.randint(0,1)
    arr.append(ran)
    if (genshin(ran,arr[i])):
        prob+=1
    i+=1
print (prob/n)