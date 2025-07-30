
// imagine not haveing lists 
// what an ass language why would anyone use it 
// cringe moment

//ahhhhh samvar i cant read this code at all

class friends
{
    public static void main(String args[])
    {
        System.out.println("\f");
        int sample_size = 1000;
        int size_of_participents_who_follow_rule=0;
        String a[]= new String[sample_size];
        int b[]= new int[sample_size];
        int c[]= new int[sample_size];
        Double avg_number_of_friends_of_friends = 0.0;
        Double avg_number_of_friends = 0.0;
        Double avg_friends = 7.0;
        Double prob = avg_friends/sample_size;
        for (int i=0; i<sample_size; i++)
        {
            a[i] = " ";
        }
        for (int i=0; i<sample_size; i++)
        {
            for(int j=(i+1);j<sample_size; j++)
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
        for (int i=0; i<sample_size; i++)
        {
            for (int j=1; j<sample_size; j++)
            {
                if (a[i].contains(" ".concat(String.valueOf(j)).concat(" ")))
                {
                    c[i]=c[i]+b[j];
                }
            }
        }
        for (int i=0; i<sample_size; i++)
        {
            avg_number_of_friends_of_friends = avg_number_of_friends_of_friends + c[i];
        }
        avg_number_of_friends_of_friends = avg_number_of_friends_of_friends /sample_size;
        for (int i=0; i<sample_size; i++)
        {
            avg_number_of_friends = avg_number_of_friends + b[i];
        }
        avg_number_of_friends = avg_number_of_friends/sample_size;
        for (int i=0; i<sample_size; i++)
        {
            if (c[i]>(b[i]*b[i]))
            {
                size_of_participents_who_follow_rule++;
            }
        }
        if (size_of_participents_who_follow_rule>500){
            System.out.println(size_of_participents_who_follow_rule);
            System.out.println(avg_number_of_friends_of_friends );
            System.out.println(avg_number_of_friends);
            System.out.println(prob);
            System.exit(0);
        }
        else
        {
            System.out.println(size_of_participents_who_follow_rule);
            System.out.println(avg_number_of_friends_of_friends );
            System.out.println(avg_number_of_friends);
            System.out.println(prob);
            System.exit(0);
        }
    }
}