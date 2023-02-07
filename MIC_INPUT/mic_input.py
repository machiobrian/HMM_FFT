import pyaudio
import numpy as np 
import librosa
import timeit
import struct
import matplotlib.pyplot as plt 

formart  = pyaudio.paFloat32
sample_freq = 44100
frame_size = 1024
no_frames = 220

p = pyaudio.PyAudio()
print("running...")

# fetch our stream
stream = p.open(
    format=formart,
    channels=1,
    rate=sample_freq,
    input=True,
    frames_per_buffer=frame_size
)

data = stream.read(no_frames*frame_size)
decoded = np.frombuffer(data, np.float32)

stream.stop_stream()
stream.close()
p.terminate()
print("done!")

plt.plot(decoded)
plt.show()

# start timing
tic = timeit.default_timer()

n_fft = int(0.025*sample_freq)
hop_length = int(0.01*sample_freq)

mel_spec_rec = librosa.feature.melspectogram(
    y = decoded/1.0,
    sr = sample_freq,
    n_fft= n_fft,   
    hop_length = hop_length,
    n_mels = 40
)

log_mel_spec = np.log(mel_spec_rec)
rec_signal = log_mel_spec.T

# stop timer
toc = timeit.default_timer()

print(toc-tic)

fig, ax = plt.subplots(figsize=(9, 5))
ax.imshow(log_mel_spec, origin="lower", interpolation="nearest");
plt.ylabel("Feature dimensions")
plt.xlabel("Frames");