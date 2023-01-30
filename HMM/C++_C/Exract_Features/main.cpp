#include <stdio.h>
#include <stdlib.h>
#include "hmm.h"

#define NUM_STATES 5
#define NUM_OBSERVATIONS 3

int main(int argc, char *argv[])
{
    // define HMM model
    double initialProbs[NUM_STATES] = {0.2, 0.4, 0.2, 0.1, 0.1};
    double transitionProbs[NUM_STATES][NUM_STATES] = {
        {0.5, 0.2, 0.2, 0.1, 0.0},
        {0.1, 0.6, 0.1, 0.1, 0.1},
        {0.0, 0.1, 0.6, 0.2, 0.1},
        {0.1, 0.1, 0.1, 0.5, 0.2},
        {0.2, 0.0, 0.2, 0.4, 0.2}
    };
    double observationProbs[NUM_STATES][NUM_OBSERVATIONS] = {
        {0.1, 0.6, 0.3},
        {0.3, 0.4, 0.3},
        {0.5, 0.1, 0.4},
        {0.2, 0.4, 0.4},
        {0.6, 0.2, 0.2}
    };

    // define HMM model data structures
    hmm_model_t model;
    model.numStates = NUM_STATES;
    model.initialProbs = initialProbs;
    model.transitionProbs = transitionProbs;
    model.observationProbs = observationProbs;

    // define observations
    int observations[4] = {1, 0, 1, 2};

    // compute maximum likelihood state sequence
    int stateSequence[4];
    hmm_viterbi(model, 4, observations, stateSequence);

    // print result
    printf("Maximum likelihood state sequence: ");
    for (int i = 0; i < 4; i++) {
        printf("%d ", stateSequence[
