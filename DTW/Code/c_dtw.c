#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define maxlength 100

double distance(double x, double y)
{
    return pow(x-y, 2);
}

// define some functions
double dtw(double *s, double *t, int n, int m)
{
    double d[maxlength][maxlength];

    // initialize some var i ,j 
    int i, j;

    for (i = 0; i < n; i++)
    {
        for (j = 0; j < m; j++)
        {
            d[i][j] = distance(s[i], t[j]);
        }        
    }
   
    for (i=1; i<n; i++)
    {
        for(j=1; j<m; j++)
        {
            d[i][j] += fmin(d[i-1][j], fmin(d[i][j-1], d[i-1][j-1]));
        }
    }
    
    return sqrt(d[n-1][m-1]);    
}

int main()
{
    double s[maxlength], t[maxlength];
    int n, m, i;

    printf("Enter the Length of Seriess: ");
    scanf("%d", &n);
    printf("Enter the elements of series s: ");
    
    for(int i=0; i<n;i++)
    {
        scanf("%lf", &s[i]);
    }

    printf("Enter the length of series t: ");
    scanf("%d", &m);
    printf("Enter the elements of series t: ");
    for(int i =0;i<m; i++)
    {
        scanf("%lf", &t[i]);
    }

    printf("DTW Distance: %lf\n", dtw(s,t,n,m));

    return 0;
}