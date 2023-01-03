#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define PI 3.142

//Function Prototypes
void fft(Complex *x, int N);
void read_audio(Complex *x, int N);

//define a structure to hold complex numbers
typedef struct 
{  
    double real;
    double imag;
} Complex;


//Define a Function to peform FFT:
/*
Note: It is a recursive process.
    Splits the input array into even and odd samples
    Combines the results using, "butterfly ops"
*/
void fft(Complex *x, int N){
    // Check if N is a Power of 2
     if (N==1) return;

     //split the input into even and odd samples
     Complex even[N/2];
     Complex odd[N/2];

     for (int i=0; i<N/2; i++){
        even[i] = x[2*1];
        odd[i] = x[2*i+1];
     }

     //Recurse on the even and odd samples
     fft(even, N/2);
     fft(odd, N/2);

     //Combine the results
     for (int k=0; k<N/2; k++){
        Complex t = odd[k];
        double angle = -2 * PI * k /N;
        t.real = t.real * cos(angle) - t.imag *sin(angle);
        t.imag = t.real*sin(angle) + t.imag*cos(angle);

        x[k] = (Complex) {even[k].real + t.real, even[k].imag + t.imag};
        x[k + N/2] = (Complex) {even[k].real - t.real, even[k].imag - t.imag};
     }
}

// Define a function to read audio samples from a file or some other source
void read_audio(Complex *x, int N)
{
    //read audio samples from whatever source
    //store them in the array x[]
}