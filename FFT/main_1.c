#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "kiss_fft.h"

#define N 256 // size of FFT
#define PI 3.14159265358979323846

int main(int argc, char *argv[])
{
    kiss_fft_cpx in[N], out[N]; // complex number data type
    kiss_fft_cfg cfg; // configuration structure
    int i;

    // initialize input with a sine wave
    for (i = 0; i < N; i++) {
        in[i].r = cos(2*PI*i/N);
        in[i].i = 0;
    }

    // initialize FFT configuration
    cfg = kiss_fft_alloc(N, 0, NULL, NULL);

    // perform FFT
    kiss_fft(cfg, in, out);

    // print results
    for (i = 0; i < N; i++) {
        printf("%d %f %f\n", i, out[i].r, out[i].i);
    }

    free(cfg);
    return 0;
}
