package learnjava;
// imagine not haveing lists 
// what an ass language why would anyone use it 
// cringe moment
class friends
{
    public static void main(String args[])
    {
        System.out.println("\f");
        int n = 1000;
        int m=0;
        String a[]= new String[n];
        int b[]= new int[n];
        int c[]= new int[n];
        Double avg = 0.0;
        Double agg = 0.0;
        Double prob = 0.007;
        for (int i=0; i<n; i++)
        {
            a[i] = " ";
        }
        for (int i=0; i<n; i++)
        {
            for(int j=(i+1);j<n; j++)
            {
                Double p = Math.random();
                if(p<prob)
                {
                    a[i]=a[i].concat(String.valueOf(j).concat(" "));
                    a[j]=a[j].concat(String.valueOf(i).concat(" "));
                    b[i]=b[i]+1;
                    b[j]=b[j]+1;
                }
;
            }
        }
        for (int i=0; i<n; i++)
        {
            for (int j=1; j<n; j++)
            {
                if (a[i].contains(" ".concat(String.valueOf(j)).concat(" ")))
                {
                    c[i]=c[i]+b[j];
                }
            }
        }
        for (int i=0; i<n; i++)
        {
            avg = avg + c[i];
        }
        avg = avg/n;
        for (int i=0; i<n; i++)
        {
            agg = agg + b[i];
        }
        agg = agg/n;
        for (int i=0; i<n; i++)
        {
            if (c[i]>(b[i]*b[i]))
            {
                m++;
            }
        }
        if (m>500){
            System.out.println(m);
            System.out.println(avg);
            System.out.println(agg);
            System.out.println(prob);
            System.exit(0);
        }
        else
        {
            System.out.println();
        }
    }
}