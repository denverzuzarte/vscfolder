import math
class cost:
    def costfunc(prob,answer):
     cost=0;
     y=0
     for x in prob :

         cost=cost+(prob[y]-answer[y])**2;
         y=y+1;
     return math.pow(cost,.5);