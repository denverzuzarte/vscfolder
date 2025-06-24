import math
import random
import trainer
import realset
def maxi(count):
    x=0;k=0;max=0;
    while x<10:
        if max<=count[x]:
            max=count[x];
            k=x;
        x=x+1;
    return k,max;
#starter
ans=math.floor(random.random()*10);
n=math.floor(random.random()*1000);
random_file=(realset.files[ans][n]);
# Get pixels list here
pixels=trainer.trainer(random_file);
a=.5;
# giving random values to weights
weights2=[];
i=0;
while i<16:
    j=0;
    weights2.append([]);
    while j<28*28:
        weights2[i].append(a*(random.random()*2-1));
        j=j+1;
    i=i+1;

weights3=[];
i=0;
while i<16:
    j=0;
    weights3.append([]);
    while j<16:
        weights3[i].append(a*(random.random()*2-1));
        j=j+1;
    i=i+1;

weights4=[];
i=0;
while i<10:
    j=0;
    weights4.append([]);
    while j<16:
        weights4[i].append(a*(random.random()*2-1));
        j=j+1;
    i=i+1;
'''import pandas as pd
print(pd.DataFrame(weights2));
print(pd.DataFrame(weights3));
print(pd.DataFrame(weights4));
'''
class sigmoid:
    light=0.0;
    def func(weights, prevlayer):
        l=0.0;
        y=0;
        for x in prevlayer:
            l=l+weights[y]*x;
            y=y+1;
        light =1/(1+(math.pow(2.718, l )))
        return light;
class sigmoid_l2:
    light=0.0;
    def func(weights, prevlayer):
        l=0.0;
        y=0;
        for x in weights:
            l=l+prevlayer[(math.floor(y/28))][y%28]*x;
            y=y+1;
        light =1/(1+(math.pow(2.718, l )))
        return light;
#geting the neruron lights
x=0;neuron2=[];
while x<16:
    neuron2.append(sigmoid_l2.func(weights2[x],pixels));
    x=x+1;

x=0;neuron3=[];
while x<16:
    neuron3.append(sigmoid.func(weights3[x],neuron2));
    x=x+1;

x=0;neuron4=[];
while x<10:
    neuron4.append(sigmoid.func(weights4[x],neuron3));
    x=x+1;

answer=[0,0,0,0,0,0,0,0,0,0];
answer[ans]=1;

neuron4grad=[];neuron3grad=[];neuron2grad=[];pixelsgrad=[];
x=0
while x<784:
    neuron2grad.append(0);
    neuron3grad.append(0);
    neuron4grad.append(0);
    pixelsgrad.append(0);
    x=x+1;

# everythng below is the core logic
#this part needs to be used every time a new image is used

x=0;
while x<10:
    neuron4grad[x]=(answer[x]-neuron4[x]);
    y=0;avg1=0;
    while y<16:
        neuron3grad[y]=neuron3grad[y]+(neuron4grad[x]-weights4[x][y]*neuron3[y])/16;
        y=y+1;
    x=x+1;

x=0;
while x<16:
    y=0;avg1=0;
    while y<16:
        neuron2grad[y]=neuron2grad[y]+(neuron3grad[x]-weights3[x][y]*neuron2[y])/16;
        y=y+1;
    x=x+1;

#getting gradient of the weights
i=0
while i<16:
    j=0;
    while j<784:
        weights2[i][j]=weights2[i][j]+(pixels[(math.floor(j/28))][j%28]*neuron2grad[i])/100;
        j=j+1
    i=i+1

i=0
while i<16:
    j=0;
    while j<16:
        weights3[i][j]=weights3[i][j]+(neuron2[j]*neuron3grad[i])/100;
        j=j+1
    i=i+1
i=0
while i<10:
    j=0;
    while j<16:
        weights4[i][j]=weights4[i][j]+(neuron3[j]*neuron4grad[i])/100;
        j=j+1
    i=i+1

# end of core logic
def costfunc(prob,answer):
    cost=0;
    y=0
    for x in prob :

        cost=cost+(prob[y]-answer[y])**2;
        y=y+1;
    return cost;

# practise 1000 times
practise=0
    # new pixels
    #starter
while practise<10000 :
    ans=math.floor(random.random()*10);
    n=math.floor(random.random()*1000);
    random_file=(realset.files[ans][n]);
    # Get pixels list here
    pixels=trainer.trainer(random_file);
    a=.5;

    # new stuff
    #geting the neruron lights
    x=0;neuron2=[];
    while x<16:
        neuron2.append(sigmoid_l2.func(weights2[x],pixels));
        x=x+1;

    x=0;neuron3=[];
    while x<16:
        neuron3.append(sigmoid.func(weights3[x],neuron2));
        x=x+1;

    x=0;neuron4=[];
    while x<10:
        neuron4.append(sigmoid.func(weights4[x],neuron3));
        x=x+1;

    answer=[0,0,0,0,0,0,0,0,0,0];
    answer[ans]=1;

    neuron4grad=[];neuron3grad=[];neuron2grad=[];pixelsgrad=[];
    x=0
    while x<784:
        neuron2grad.append(0);
        neuron3grad.append(0);
        neuron4grad.append(0);
        pixelsgrad.append(0);
        x=x+1;

    # everythng below is the core logic
    #this part needs to be used every time a new image is used

    x=0;
    while x<10:
        neuron4grad[x]=-(answer[x]-neuron4[x]);
        y=0;avg1=0;
        while y<16:
            neuron3grad[y]=neuron3grad[y]+(neuron4grad[x]*weights4[x][y])/16;
            y=y+1;
        x=x+1;

    x=0;
    while x<16:
        y=0;avg1=0;
        while y<16:
            neuron2grad[y]=neuron2grad[y]+(neuron3grad[x]*weights3[x][y])/16;
            y=y+1;
        x=x+1;
    #getting gradient of the weights
    i=0
    while i<16:
        j=0;
        while j<784:
            k=0;
            while k<784:
                weights2[i][j]=weights2[i][j]+(pixels[(math.floor(j/28))][j%28]*neuron2grad[i])/100;
                k=k+1;
            j=j+1;
        i=i+1;
    i=0;
    while i<16:
        j=0;
        while j<16:
            k=0;
            while k<16:
                weights3[i][j]=weights3[i][j]+(neuron2[k]*neuron3grad[i])/100;
                k=k+1;
            j=j+1;
        i=i+1;
    i=0
    while i<10:
        j=0;
        while j<16:
            k=0;
            while k<16:
                weights4[i][j]=weights4[i][j]+(neuron3[j]*neuron4grad[i])/100;
                k=k+1;
            j=j+1;
        i=i+1;
    practise=practise+1;
    expense=costfunc(neuron4,answer)
    k,max=maxi(neuron4);
    print('|',end='');
    if (practise % 40==0):
        print(practise,' - ',ans,' - ',expense,' my guess is - ',k,end='');
'''   #check 1 item(s) see if the machine learnt anything
    check=0;
    #while check<10:
    random_file=(input("enter the path of the file - "));
    ans=(random_file[40]);
    print(ans);
    # Get pixels list here
    #pixels=trainer.trainer(random_file);
    a=.5;

    # new stuff
    #geting the neruron lights
    x=0;neuron2=[];
    while x<16:
        neuron2.append(sigmoid_l2.func(weights2[x],pixels));
        x=x+1;

    x=0;neuron3=[];
    while x<16:
        neuron3.append(sigmoid.func(weights3[x],neuron2));
        x=x+1;

    x=0;neuron4=[];
    while x<10:
        neuron4.append(sigmoid.func(weights4[x],neuron3));
        x=x+1;

    answer=[0,0,0,0,0,0,0,0,0,0];
    answer[int(ans)]=1;

    neuron4grad=[];neuron3grad=[];neuron2grad=[];pixelsgrad=[];
    x=0
    while x<784:
        neuron2grad.append(0);
        neuron3grad.append(0);
        neuron4grad.append(0);
        pixelsgrad.append(0);
        x=x+1;

    # everythng below is the core logic
    #this part needs to be used every time a new image is used

    x=0;
    while x<10:
        neuron4grad[x]=(answer[x]-neuron4[x]);
        y=0;avg1=0;
        while y<16:
            neuron3grad[y]=neuron3grad[y]+(neuron4grad[x]-weights4[x][y]*neuron3[y])/16;
            y=y+1;
        x=x+1;

    x=0;
    while x<16:
        y=0;avg1=0;
        while y<16:
            neuron2grad[y]=neuron2grad[y]+(neuron3grad[x]-weights3[x][y]*neuron2[y])/16;
            y=y+1;
        x=x+1;
        i=i+1
        import digit_sorter
        k,max=digit_sorter.maxi(neuron4)
    print('my guess is - ',k);
    check=check+1;  .'''