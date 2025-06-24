class thrusters:
    def __init__(self,co,thrustertype):
        self.coeff=co;
        self.tt=thrustertype;
    # type is 1=yaw 2=pitch 3=front 4=up
    def acc(self,type,inten):
        if type==1:
            print("yaw");
            if self.tt==1:
                print("left");
            elif self.tt==2:
                print("front");
            elif self.tt==3:
                print("right");
            elif self.tt==4:
                print("back");
        elif type==2:
            print("pitch");
            if self.tt==1:
                print("left");
            elif self.tt==2:
                print("front");
            elif self.tt==3:
                print("right");
            elif self.tt==4:
                print("back");
        elif type==3:
            print("forward");
            if self.tt==1:
                print("left");
            elif self.tt==2:
                print("front");
            elif self.tt==3:
                print("right");
            elif self.tt==4:
                print("back");
        elif type==4:
            print("up");
            if self.tt==1:
                print("left");
            elif self.tt==2:
                print("front");
            elif self.tt==3:
                print("right");
            elif self.tt==4:
                print("back");
        
    def force(self,acc): 
        force=self.coeff*acc;
        return force;
leftT=thrusters(1.01,1);
print(leftT.force(leftT.acc(2,3)));