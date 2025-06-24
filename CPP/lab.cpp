#include <iostream>
using namespace std;
bool square(int sudoku[][9])
{
    bool boolval=true;
    int i=0,j=0,k=0;
    while (i<9)
    {
        j=0;
        while (j<9)
        {
            k=0;
            while(k<9)
            {
            if (sudoku[i][j]!=sudoku[i/3+k/3][j/3+j%3])
            {
                boolval = false; 
            }
            j++;
            }
        }
        i++;
    }
    return boolval;
}
int main()
{
    int sudoku[9][9];
    int i=0,j=0,k=0,cval;
    while (i<9)
    {
        j=0;
        while (j<9)
        {
            cin >> sudoku[i][j];
            j++;
        }
        i++;
    }
        
    i=0;
    while (i<9)
    {
        j=0;
        while (j<9)
        {
            k=0;
            cval=sudoku[i][j];
            while (k<9)
            {
                
                if ((cval==sudoku[k][j]&&(k!=i)) || (cval==sudoku[i][k]&&(k!=j)) || square(sudoku))
                {
                    cout << "False";
                    exit(0);
                }
                k++;
            }
            j++;
        }
        i++;
        
    }
} // namespace std