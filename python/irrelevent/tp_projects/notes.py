'''
print ("hello world");
myint=5;
myfloat=10.0;
mystr="hello broski";
print(myint + myfloat);
num = str(myint);
print(num+mystr);
mylist= ['a','b','c','d','e','f','g','?','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y'];
mylist.append('z');
length=len(mylist);
mylist[7]='h';
print ("here is a %s and here is another %d " % ('hello',myint));
#%s - String (or any object with a string representation, like numbers)
#%d - Integers
#%f - Floating point numbers
#%.<number of digits>f - Floating point numbers with a fixed amount of digits to the right of the dot.
length=len(mystr);
position=mystr.index("o");
rep=mystr.count('l');
littlestring=mystr[3:7:1]
print(littlestring);
print(mystr[::-1]);
bool=True
if bool :
    print("here")
elif num :
    print("not here either")
else :
    print("not here")
x=3
y=3
x2=3
y2=x2
print(x2 is y2)
print(x is y)
print(not False)
for x in mylist:
    print(x)
for x in range(1,10,2):
    print(x)
i=0
while i<10:
    i=i+1
    print(i)
    if i==6 :
        break
    else :
        continue
# functions
def my_function(myvar):

    print ("Good function")
    return myvar+3
a=my_function(7); #called here aswell so even printing will occur
my_function(1)
'''
#classes
class myclass:
    var2='i';
    def classfunction(self):
        print("this is in the class"+myclass.var2);

#calling the class
myobject=myclass()
print(myobject.var2=='i')
myobject.classfunction();
'''
#__init__() function - gets called when an instance is created
class gayshit:

    def __init__(self, gay):
        print("yay")
        self.h = gay

    def bs(self):
        return self.h
    
var=gayshit(8)
#print(var.bs())

#dictionaries
dictionary={}
dictionary["word 1"]="meaning 1"
dictionary["word 2"]="meaning 2"
dictionary["word 3"]="meaning 3"
print(dictionary)
for word,meaning in dictionary.items():
    print(word +" "+meaning)
del dictionary["word 1"]; # or dictionary.pop("word 1")
print( dictionary)

#how to recieve input
name=input('what is your name ? ');
fav_color=input("what is your fav color ")
print(name+' likes '+fav_color);

#Math functions
import math
x=-2.9
n=2
r=1
y=input()
abs(x) 
ceiling=math.ceil(x)
floor=math.floor(x);
choose=math.comb(n,r); # returns nCr 
print(choose);
abs=math.fabs(x); # returns abs val of x
math.factorial(n);#returns factorial
bool2=(n%r==math.fmod(n,r));#returns true
if(x or y):
    print (x)

#modules and packages
import draw
print(draw.stuff())
#always make sure you run every module you have made
from draw import draw2 # imports class draw 2 from draw module
from draw import * #imports every all classes from module
drawing1=draw2();
drawing1.draws();
i=0
while i==0:
    print("");
    i=i+1;
if(not i) :
    import draw_visual as drawing
else:
    import draw as drawing
drawing.draw2()


# numpy arrays
import numpy as n;
#lists to numpy arrays
exlist=[1,2,3,4,5,4,3,3,2]
numpy_arrays=n.array(exlist)
print(numpy_arrays);
height = [1.87,  1.87, 1.82, 1.91, 1.90, 1.85]
weight = [81.65, 97.52, 95.25, 92.98, 86.18, 88.45]
nh= n.array(height);
nw= n.array(weight);
bmi=nw / nh ** 2;
print (bmi);
print (bmi>24);
print (bmi[bmi>24]);#subsetting
'''
# pandas basics
dict = {"country": ["Brazil", "Russia", "India", "China", "South Africa"],
       "capital": ["Brasilia", "Moscow", "New Dehli", "Beijing", "Pretoria"],
       "area": [8.516, 17.10, 3.286, 9.597, 1.221],
       "population": [200.4, 143.5, 1252, 1357, 52.98] }

import pandas as pd
brics = pd.DataFrame(dict)
print(brics)
print(dict);