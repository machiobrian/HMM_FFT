
from ulab import numpy as np

a = np.array(range(5), dtype=np.float)
b = np.array(range(25),
              dtype=np.uint8).reshape((5, 5))

np.ndinfo(a)
print('\n')
np.ndinfo(b)