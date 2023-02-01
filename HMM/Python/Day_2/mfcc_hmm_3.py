import librosa
import numpy as np
from hmmlearn import hmm

# Load the .wav file
wav_file, sr = librosa.load("", sr=None)

# Split the audio into smaller frames
frames = librosa.util.frame(wav_file, frame_length=1024, hop_length=512).T

# Compute the MFCCs for each frame
mfccs = np.array([librosa.feature.mfcc(f, sr=sr, n_mfcc=13) for f in frames])

# Train an HMM model
model = hmm.GaussianHMM(n_components=10, covariance_type="diag")
model.fit(mfccs)

# Compute the MFCCs for a new, unseen audio file
new_wav_file, sr = librosa.load("path/to/new/wav/file.wav", sr=None)
new_frames = librosa.util.frame(new_wav_file, frame_length=1024, hop_length=512).T
new_mfccs = np.array([librosa.feature.mfcc(f, sr=sr, n_mfcc=13) for f in new_frames])

# Pass the MFCCs through the trained HMM and calculate the likelihood score
scores = [model.score(new_mfccs) for model in models]

# Choose the model with the highest likelihood score as the output
output = models[np.argmax(scores)]
