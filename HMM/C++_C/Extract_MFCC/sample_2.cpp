// calculate the mel freq bins for MFCC

#include <iostream>
#include <vector>
#include <algorithm>
#include <math.h>
#include <fftw3.h>

const int sampling_rate = 16000; 
const int frame_size = 512;
const int overlap = 256; // overlap btn frames in samples
const int num_mfcc = 13; // number of mfcc to extract
const int num_filters = 40; // number of filters in the mel filterbanks

// define a function to compute the mel freq scale
std::vector<double> compute_mel_scale(int num_filters, int min_freq, int max_freq)
{
    double mel_min = 1125.0 * log(1.0 + min_freq / 700.0);
    double mel_max = 1125.0 * log(1.0 + max_freq / 700.0);
    double mel_delta = (mel_max - mel_min) / (num_filters+1);

    std::vector<double> mel_scale(num_filters);
    
    for (int i = 0; i < num_filters; i++)
    {
        double mel_freq = mel_min + (i+1) * mel_delta;
        mel_scale[i] = 700.0 * (exp(mel_freq / 1125.0) - 1.0);
    }
    return mel_scale;
}

// define a function to compute the triangualar filters for the Mel filterbanks
std::vector<std::vector<double>> computer_triangular_filters(int num_filters, int num_fft_bins, double min_freq, double max_freq)
{   
    std::vector<double> mel_scale = compute_mel_scale(num_filters, min_freq, max_freq);

    std::vector<std::vector<double>> filters(num_filters, std::vector<double>(num_fft_bins, 0.0));
    for (int i = 0; i < num_filters; i++)
    {
        double center = mel_scale[i];
        double left = (i == 0) ? mel_scale[i] : mel_scale[i-1];
        double right = (i == num_filters - 1) ? mel_scale[i] : mel_scale[i+1];

        for (int j = 0; j < num_fft_bins; j++)
        {
            double freq = j * sampling_rate / num_fft_bins;

            if (freq >= left&& freq <= center)
            {
                filters[i][j] = (freq - left) / (center - left);
            }
            else if (freq > center && freq <= center)
            {
                filters[i][j] = (right - freq) / (right - center);
            }
        }
    }
    return filters;
}