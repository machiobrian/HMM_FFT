"""
A - state transition matrix
B - emission probability matrix
pi - initial state probability distribution
        (A,B,pi) = lambda
Compute the Score - find the probability of a particular chain of observations O given
our known model lambda

we are computing the score naively since - calculate the probability for every possible 
chain X.

Q - latent states
O - possible observation states
"""

from itertools import product
from functools import reduce

from Prob_Matrix import ProbabilityMatrix, ProbabilityVector
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

class HiddenMarkovChain_Uncover(HiddenMarkovChain_Simulation):
    def _alphas(self, observations: list) -> np.ndarray:
        alphas = np.zeros((len(observations), len(self.states)))
        alphas[0, :] = self.pi.values * self.E[observations[0]].T

        for t in range(1, len(observations)):
            alphas[t, :] = (alphas[t-1, :].reshape(1,-1) @ self.T.values) \
            * self.E[observations[t]].T
            return alphas
    def _betas(self, observations: list) -> np.ndarray:
        betas = np.zeros((len(observations), len(self.states)))
        betas[-1, :] = 1
        for t in range(len(observations)-2, -1, -1):
            betas[t, :] =  (self.T.values @ (self.E[observations[t+1]] \
            * betas[t+1, :].reshape(-1, 1))).reshape(1,-1)
            return betas
    def uncover(self, observations:list) -> list:
        alphas = self._alphas(observations)
        betas = self._betas(observations)
        maxargs = (alphas*betas).argmax(axis=1)
        return list(map(lambda x: self.states[x], maxargs))

class HiddenMarkovLayer(HiddenMarkovChain_Uncover):
    # digamma method, performes all neccesary calculations
    def _digammas(self, observations: list) -> np.ndarray:
        L, N = len(observations), len(self.states)
        digammas = np.zeros((L-1,N,N))

        alphas = self._alphas(observations)
        betas = self._betas(observations)
        score = self.score(observations)

        for t in range(L-1):
            P1 = (alphas[t,:].reshape(-1,1)* self.T.values)
            P2 = self.E[observations[t+1]].T * betas[t+1].reshape(1,-1)
            digammas[t, :, :] = P1*P2 / score
            return digammas
# --------------------------------------------------------------------------- #
# Model Training Summary:
# Intialize A,B,pi
# Calculate gamma(i,j)
# Update models A,B,pi
# Repeat 2/3 until the score no longer increases

class HiddenMarkovModel:
    def __init__(self, hml: HiddenMarkovLayer):
        self.layer = hml
        self._score_init = 0
        self.score_history = []

    @classmethod
    def initialize(cls, states: list, observables:list):
        layer = HiddenMarkovLayer.initialize(states, observables)
        return cls(layer)
    
    def update(self, observations:list) -> float:
        alpha = self.layer._alphas(observations)
        beta = self.layer._betas(observations)
        digamma = self.layer._digammas(observations)
        score = alpha[-1].sum()
        gamma = (alpha*beta)/score

        L = len(alpha)
        obs_idx = [self.layer.observables.index(x) for x in observations]
        capture = np.zeros((L, len(self.layer.states), len(self.layer.observables)))
        for t in range(L):
            capture[t, :, obs_idx[t]] = 1.0
        pi = gamma[0]
        T = digamma.sum(axis=0) / gamma[:-1].sum(axis=0).reshape(-1,1)
        E = (capture*gamma[:,:,np.newaxis]).sum(axis=0)/gamma.sum(axis=0).reshape(-1,1)
        
        self.layer.pi = ProbabilityVector.from_numpy(pi, self.layer.states)
        self.layer.T = ProbabilityMatrix.from_numpy(T, self.layer.states, self.layer.states)
        self.layer.E = ProbabilityMatrix.from_numpy(E, self.layer.states, self.layer.observables)
        return score
    
    def train(self, observations: list, epochs:int, tol=None):
        self._score_init = 0
        self.score_history = (epochs + 1) * [0]
        early_stopping = isinstance(tol, (int, float))

        for epoch in range(1, epochs+1):
            score = self.update(observations)

            print("Training ... epoch = {} out of {}, score = {}".format(epoch, epochs, score))

            if early_stopping and abs(self._score_init - score)/ score<tol:
                print('Early stopping.')
                break
            self._score_init = score
            self.score_history[epoch] = score