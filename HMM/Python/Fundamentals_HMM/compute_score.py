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

from itertools import product
from functools import reduce

from Prob_Matrix import ProbabilityMatrix

class HiddenMarkovChain:
    def __init__(self, T,E,pi):
        self.T = T #transmission matrix A
        self.E = E # emission matrix B
        self.pi = pi
        self.states  = pi.states
        self.observables = E.observables
    
    def __repr__(self):
        return "HML states: {} - observables: {}.".format(
            len(self.states), len(self.observables)
        )

    @classmethod
    def initialize(cls, states:list, observables:list):
        T = ProbabilityMatrix.initialize(states, states)
        E = ProbabilityMatrix.initialize(states, observables)
        pi = ProbabilityVector.initialize(states)
        return cls(T,E,pi)

    def _create_all_chains(self, chain_length):
        return list(product(*(self.states,)*chain_length))

    def score(self, observations:list) -> float:
        def mul(x,y):return x*y

        score = 0
        all_chains = self._create_all_chains(len(observations))
        for idx, chain in enumerate(all_chains):
            expanded_chain = list(zip(chaink, [self.T.states[0] + list(chain)]))
            expanded_obser = list(zip(observations, chain))

            p_observations = list(map(lambda x: self.E.df.loc[x[1], x[0]], expanded_obser))
            p_hidden_state = list(map(lambda x: self.T.df.loc[x[1], x[0]], expanded_chain))

            p_hidden_state[0]  = self.pi[chain[0]]

            score += reduce(mul, p_observations) * reduce(mul, p_hidden_states)
            return score
            