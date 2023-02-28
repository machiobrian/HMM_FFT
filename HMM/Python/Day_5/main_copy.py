"""
we intend to test this one out on the original dataset
"""

# input-folder : /home/ix502iv/Documents/Audio_Trad/HMM/Python/Day_5/data/audio
import os
import argparse

import numpy as np 
from scipy.io import wavfile
from hmmlearn import hmm
from python_speech_features import mfcc

# function to parse input arguments
def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Trains the HMM Classifier")
    parser.add_argument(
        "--input-folder",
        dest="input_folder",
        required=True,
        help="Input folder containing the audio files in subfolders")
    return parser

# define a class to model HMMs

class HMMTrainer(object):
    def __init__(self,model_name='GaussianHMM', n_components=4, cov_type='diag', n_iter=5000):
        self.model_name = model_name
        self.n_components = n_components
        self.cov_type = cov_type
        self.n_iter = n_iter
        self.models = [] # where we are going to store all the models for words we want to identify

        if self.model_name == 'GaussianHMM':
            self.model = hmm.GaussianHMM(
                n_components=self.n_components,
                covariance_type=self.cov_type,
                n_iter=self.n_iter
                )
        else:
            raise TypeError('Invalid Model Type')

    # X is a 2D numpy array where each row is 13D : look into this one keenly.
    def train(self, X):
        np.seterr(all='ignore')
        self.models.append(self.model.fit(X))

    # Run the model on input data : try and see how our model works
    def get_score(self, input_data):
        return self.model.score(input_data)
    
if __name__=='__main__':
    args = build_arg_parser().parse_args()
    input_folder = args.input_folder
    
    hmm_models = [] # initiate a variable to hold all the hmm models

    # parse the input dir
    for dirname in os.listdir(input_folder):
        # get the name/link of the subfolder
        subfolder = os.path.join(input_folder, dirname)
        if not os.path.isdir(subfolder): # if not a dir, pass/skip it
            continue

        # extract the label : another important concept
        label = subfolder[subfolder.rfind('/') + 1:]
        # print(label)

        # initialize variables
        X = np.array([])
        y_words = []

        # define a function to normalize audio data
        def normalize_audio(audio):
            # get the mac abs value
            max_abs = np.max(np.abs(audio))
            print(max_abs)
            # divide audio data by max_abs to normalize the audio data
            return audio / max_abs

        # Iterate through audio files leaving 1 file for testing in each class
        for filename in [x for x in os.listdir(subfolder) if x.endswith('.wav')][:-1]:
            # read the input file and extract the sampling freq and audio_data
            filepath = os.path.join(subfolder, filename)
            sampling_frequency, audio = wavfile.read(filepath)

            # extract the mfcc features
            mfcc_features = mfcc(audio, sampling_frequency,nfft=512)

            # append to the X variable
            if len(X) == 0:
                X = mfcc_features
            else:
                X = np.append(X, mfcc_features, axis=0)

            # Append the label
            y_words.append(label)
            # print('X.shape = ', X.shape)

        # Train and Save HMM model
        hmm_trainer = HMMTrainer()
        hmm_trainer.train(X)
        hmm_models.append((hmm_trainer, label))
        # free up memory
        hmm_trainer = None

    # test files
    input_files = [
        "/home/ix502iv/Documents/Audio_Trad/HMM/Python/Day_5/data/audio/apple/apple.wav",
        "/home/ix502iv/Documents/Audio_Trad/HMM/Python/Day_5/data/audio/banana/banana.wav"
    ]

    # classify the input data
    for input_file in input_files:
        # read & extract from the input files
        sampling_frequency, audio_data = wavfile.read(input_file)

        # extract mfcc features
        mfcc_features = mfcc(audio_data, sampling_frequency, nfft=512)
        

        # define variabes
        max_score = 0.0 # initially None
        output_label = "unknown"

        # iterate through all HMM Models and pick the one with the highest score
        for item in hmm_models:
            hmm_model, label = item 
            # print(label) # --------------------------------
            score = hmm_model.get_score(mfcc_features)
            # print(score)
            if score > max_score:
                max_score = score 
                output_label = label
                

        # Print the output
        print("\nTrue:", input_file[input_file.rfind('/')+1:input_file.rfind('.')])
        print("Predicted:", output_label)    