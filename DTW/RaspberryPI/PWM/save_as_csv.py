from scipy.fft import fft
# fft to perform a fast fourier on the encoded audio sample
import numpy as np 

# fourirer transform the encoded output
fourirer_trans = fft(encoded_sample)
abs_fourier_trans = fft(encoded_sample)

# extract the fourier_trans values and save as a csv file
np.savetxt("extracted_values.csv", a, delimiter=",")
np.savetxt("extracted_abs_values.csv",a,delimiter=",") # get the absolute values also
