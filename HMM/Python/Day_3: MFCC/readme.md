1. import the required libs : librosa, hmmlearn `DONE`
2. extract mfcc features from a .wav file `DONE`
3. train a hmm: `DONE`
    * feed it with training data - in mfcc format (repeat step 2) (for our dictionary)

4. validate our training
    * load the test audio file and extract mfcc features.
    * use `predict` or `predict_proba` method of the HMM model to predict the most likely sequence of Hidden states given mfcc features
    * map the sequence of hidden states to the coresponding labels - to get the predicted transcription.