from ulab import numpy
from ulab import scipy


I = numpy.array([[3, 0, 0, 0], 
                 [2, 1, 0, 0], 
                 [1, 0, 1, 0], 
                 [1, 2, 1, 8]])
j = numpy.array([4, 2, 4, 2])

# print(scipy.linalg.cho_solve(I,j))

# FFT Speed.
x = numpy.linspace(0, 10, num=1024)
y = numpy.sin(x)

# @timeit
def np_fft(y):
    return numpy.fft.fft(y)
a, b = np_fft(y)