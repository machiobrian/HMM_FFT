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
import numpy as np 

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
            expanded_chain = list(zip(chain, [self.T.states[0]] + list(chain)))
            expanded_obser = list(zip(observations, chain))

            p_observations = list(map(lambda x: self.E.df.loc[x[1], x[0]], expanded_obser))
            p_hidden_state = list(map(lambda x: self.T.df.loc[x[1], x[0]], expanded_chain))

            p_hidden_state[0]  = self.pi[chain[0]]

            score += reduce(mul, p_observations) * reduce(mul, p_hidden_state)
            return score

class HiddenMarkovChain_FP(HiddenMarkovChain):
    def _alphas(self, observations:list) -> np.ndarray:
        alphas = np.zeros((len(observations), len(self.states)))
        alphas[0, :] = self.pi.values * self.E[observations[0]].T 

        for t in range(1, len(observations)):
            alphas[t, :] = (alphas[t-1, :].reshape(1,-1) @ self.T.values) * \
                self.E[observations[t]].T
            return alphas

    def score(self, observations:list) -> float:
        alphas = self._alphas(observations)
        return float(alphas[-1].sum())

class HiddenMarkovChain_Simulation(HiddenMarkovChain):
    def run(self, length: int) -> (list, list):
        assert length >= 0, "The chain needs to be a non-negative number."
        s_history = [0] * (length + 1)
        o_history = [0] * (length + 1)
        
        prb = self.pi.values
        obs = prb @ self.E.values
        s_history[0] = np.random.choice(self.states, p=prb.flatten())
        o_history[0] = np.random.choice(self.observables, p=obs.flatten())
        
        for t in range(1, length + 1):
            prb = prb @ self.T.values
            obs = prb @ self.E.values
            s_history[t] = np.random.choice(self.states, p=prb.flatten())
            o_history[t] = np.random.choice(self.observables, p=obs.flatten())
        
        return o_history, s_history