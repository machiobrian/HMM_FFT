"""
Given the model params: 
prob of transitioning, prob of emitting observations from each state
Then, the probability of a sequence of observations is: Score
Unlike the other method of compute. This one takes adv of vectorization:

A, B, pi
"""

import numpy as np 

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