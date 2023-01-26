import array
import struct
import os
import wave 
import csv


def read_loaded_file(audio_path):
    # we are to open the .wav file
    wav_file = wave.open("audio_path", "rb")
    
    # read audio samples from the audio file
    audio_sample = wav_file.readframes(wav_file.getnframes())
    wav_file.close()

    # convert audio samples into an array
    audio_sample = array.array("h", audio_sample)
    return audio_sample

#------------------------------------------------------------------------------#
audio_sample = read_loaded_file("audio_path: enter the path to your audio sample")

# control measure
if audio_sample is None:
    exit()

# set quantized level - 16 is best 
quantization_level = 16

# quantize the audio sample
quant_audio = audio_sample

for aud in range(len(quant_audio)):
    quant_audio[aud] = int(quant_audio[aud]/(2**15/quantization_level)) * (2**15/quantization_level)

encod_audio = struct.pack("h"*len(quant_audio), *quant_audio)

# we are going to write the encod_audio to a csv file without going the PWM path
with open("encoded_output.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for enc_aud in encod_audio:
        writer.writerow([audio])