/* Calculate the mel frequency bins for MFCC */

#include <iostream>
#include <vector>
#include <math.h>

// define a helper function to calculate the mel-freq for a given frequency
double mel(double freq)
{
    return 2595 * log10(1+freq/700);
}

// define a helper function : calcs the inverse mel-freq for a given freq
double inverse_mel(double mel_freq)
{
    return 700 * (pow(10, mel_freq / 2595) -1);
}

int main()
{
    // define the sampling rate for the speech signal
    int sample_rate =16000;

    // define the number of mel freq bins to be used for MFCC
    int num_bins = 40;

    // define the lower and upper freq bounds for the mel bins
    double lower_freq = 30;
    double upper_freq = sample_rate/2; // 16k/2 = 8k

    // calc the mel freq bounds
    double lower_mel = mel(lower_freq);
    double upper_mel = mel(upper_freq);

    // calc the step size for the Mel-freq bins
    double mel_step = (upper_mel - lower_mel) / (num_bins+1);

    // calc the center frequencies of the mel-fre bns
    std::vector<double> center_frequencies;
    for (int i = 0; i < num_bins; i++)
    {
        double mel_center = lower_mel + (i+1)*mel_step;
        center_frequencies.push_back(inverse_mel(mel_center));
    }

    // Extract the MFCCs from the speech signal here.
    
    return 0;
}