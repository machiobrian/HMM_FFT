import array
import pyaudio
import struct

# we first configure the microphones input
input_mic = pyaudio.PyAudio()
input_stream = input_mic.open(
    format=pyaudio.paInt16,
    channels = 1,
    rate = 44000, # sampling at 44KHz, this is the standard we also use to 
                  # feed into the raspberry pi
    input = True,
    frames_per_buffer = 1024
)

# we quantize from 0-15; these are 16 levels
quantization_level = 16

# initialize a loop to read and run the data sample

audio_input = input_stream.read(1024) # read the input audio
arr_audio = array.array("h", audio_input) # convert audio_input into an array
                                          # "h" - represents a signed integer
quant_audio = arr_audio # we proceed to quantize the audio samples

for aud in range(len(quant_audio)):
    quant_audio[aud] = int(quant_audio[aud]/(2**15/quantization_level)) * (2**15/quantization_level)

encod_audio = struct.pack("h"*len(quant_audio), *quant_audio)                                          

encoded_sample = struct.pack("h"*len(quantized_sample), *quantized_sample)