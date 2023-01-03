"""
A - state transition matrix
B - emission probability matrix
pi - initial state probability distribution
        (A,B,pi) = lambda
Compute the Score - find the probability of a particular chain of observations O given
our known model lambda

we are computing the score naively since - calculate the probability for every possible 
chain X.
"""

from Prob_Matrix import ProbabilityMatrix
from Prob_Vector import ProbabilityVector
from compute_score import HiddenMarkovChain


a1 = ProbabilityVector({'1H': 0.7, '2C':0.3})
a2 = ProbabilityVector({'1H':0.4, '2C':0.6})

b1 = ProbabilityVector({'1S':0.1, '2M':0.4, '3L':0.5})
b2 = ProbabilityVector({'1S':0.7, '2M':0.2, '3L':0.1})

A = ProbabilityMatrix({'1H':a1, '2C':a2})
B = ProbabilityMatrix({'1H':b1, '2C':b2})
pi = ProbabilityVector({'1H':0.6, '2C':0.4})

hmc = HiddenMarkovChain(A,B,pi)
observations = ['1S', '2M', '3L', '2M', '1S']

print("Score for {} is {:f}".format(observations, hmc.score(observations)))