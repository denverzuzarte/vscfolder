class thruster:
    def __init__(self,coef,yaw,pitch,front,up):
        self.coeff=coef;
        self.ab=[yaw,pitch,front,up];
    def force(self,task):
        force=0;
        for i in (0,3):
            force=force + task[i]*self.ab[i];
        return force;

# type is 1=yaw 2=pitch 3=front 4=up
leftT=thruster(1.01,1,0,1,0);
tasks=[1,1,1,1];#intensity of 1=yaw 2=pitch 3=front 4=up
forceL=leftT.force(tasks);
frontT=thruster(1.01,0,1,0,1);
forceF=frontT.force(tasks);
rightT=thruster(1.01,-1,0,1,0);
forceR=rightT.force(tasks);
backT=thruster(1.01,0,-1,0,1);
forceB=backT.force(tasks);