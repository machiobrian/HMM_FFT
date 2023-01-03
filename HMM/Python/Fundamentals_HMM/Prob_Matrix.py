import pandas as pd 
import numpy as np 
from Prob_Vector import ProbabilityVector

class ProbabilityMatrix:
    def __init__(self, prob_vec_dict):
        assert len(prob_vec_dict) > 1, \
            "The number of input prob vector must be > 1"
        assert len(set([str(x.states) for x in prob_vec_dict.values()])) == 1, \
            "All internal states of all the vectors must be identical"
        assert len(prob_vec_dict.keys()) == len(set(prob_vec_dict.key())), \
            "All observables must be unique"

        self.states = sorted(prob_vec_dict)
        self.observables = prob_vec_dict[self.states[0]].states
        self.values = np.stack([prob_vec_dict[x].values for x in self.states]).squeeze()

    @classmethod
    def initialize(cls, states: list, observables: list):
        size = len(states)
        rand = np.random.rand(size, len(observables)) / (size**2) +1 /size
        rand /= rand.sum(axis=1).reshape(-1,1)
        aggr = [dict(zip(observables, rand[i,:])) for i in range(len(states))]
        pvec = [ProbabilityVector(x) for x in aggr]
        return cls(dict(zip(states, pvec)))
    
    @classmethod
    