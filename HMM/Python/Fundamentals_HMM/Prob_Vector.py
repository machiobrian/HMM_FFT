# HMM - based on probability vectors and matrices

import numpy as np
import pandas as pd 

"""
Define objets that safeguard the mathematical properties.
These objects reflect on certain elements of probability vector
"""
class ProbabilityVector:
    def __init__(self, probabilities:dict):
        states = probabilities.keys()
        probs = probabilities.values()

        assert len(states) == len(probs), \
        "The no. of probabilities must match the states. no of. (keys == values)"
        assert len(states) == len(set(states)), \
        "The names of all states must be unique"
        assert abs(sum(probs) - 1.0) < 1e-12, \
        "The probabilities must sum upto 1"
        assert len(list(filter(lambda x:0 <= x <= 1, probs))) == len(probs), \
        "Probabilities must be numbers from [0, 1] interval"
        self.states = sorted(probabilities)
        self.values = np.array(list(map(lambda x:probabilities[x], self.states))).reshape(1,-1)
        
    # A. Provide alternative ,2, ways to instantiate ProbabilityVector (@classmethod)

    @classmethod
       # instantiate randomly
    def initialize(cls, states: list):
        size = len(states)
        rand = np.random.rand(size) / (size**2) + 1 / size
        rand /= rand.sum(axis=0)
        return cls(dict(zip(states, rand)))
       # we use numpy arrays 
    @classmethod
    def from_numpy(cls, array: np.ndarray, state:list):
        return cls(dict(zip(states, list(array))))

    # B. Provide two additional methods for requesting the values - return the contents of 
    # the PV object as a dict or a pandas dataframe

    @property
    def dict(self):
        return {k:v for k, v in zip(self.states, list(self.values.flatten()))}

    @property
    def df(self):
        return pd.DataFrame(self.values, columns=self.states, index=['probability'])

    
    # C. The PV objects have to satisfy the following mathematical ops inorder to construct HMM

    def __repr__(self): #repr - class object representation in string format
        return "P({}) = {}.".format(self.states, self.values)
    def __eq__(self, other): # comparison - assertain any two PV values as equal
        if not isinstance(other, ProbabilityVector):
            raise NotImplementedError
        if (self.states == other.states) and (self.values == other.values).all():
            return True
        return False

    def __getitem__(self, state:str) -> float: # allow selecting value by the key
        if state not in self.states:
            raise ValueError("Requesting Unknown Probability state from vector.")
        index = self.states.index(state)
        return float(self.values[0, index])

    def __mul__(self, other) -> np.ndarray: # elemnt-wise multiplication
        if isinstance(other, ProbabilityVector):
            return self.values * other.values
        elif isinstance(other, (int, float)):
            return self.values * other
        else:
            NotImplementedError

    def __rmul__(self, other) -> np.ndarray: # multiplication with a scalar
        return self.__mul__(other)

    def __matmul__(self, other) -> np.ndarray: # vector-matrix multiplication
        return self.__matmul__(other)

    def __matmul__(self, other) -> np.ndarray: 
        if isinstance(other, ProbabilityMatrix): # not defined
            return self.values @ other.values

    # ndarray - represents both arrays and vectors
    def __truediv__(self, number) -> np.ndarray: # division by number
        if not isinstance(number, (int, float)):
            raise NotImplementedError
        x = self.values
        return x/number if number !=0 else x/(number + 1e-12)

    def argmax(self): # find for which state the probaility is highest
        index = self.values.argmax() #argmax - return index, of maximum values along an axis
        return self.states[index]
        