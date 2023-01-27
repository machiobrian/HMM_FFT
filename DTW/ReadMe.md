####	Medium File:
	https://betterprogramming.pub/how-to-do-speech-recognition-with-a-dynamic-time-warping-algorithm-159c2a1bb83c

####	Code Projects:
	https://www.codeproject.com/Articles/5820/Speech-Recognition
	https://www.codeproject.com/Articles/11771/Voice-Command

#### Dynamic Programming

* we are to find the minimum-cost path through matrix `dist_matrix` using dynamic programming
> Cost of a Path:

Defined as the sum of the matrix entries on that path

> The Sequence of Operation is as follows

1. Define the shape of the signal x,y and visualize
2. Define the distance matrix
3. Define the Dynamic Time Warp - `path` and `cost` function and visualize
4. Plot a distance and cost matrix subplot

#### DTW_PCM Project
1. fetch the audio data - audio signal
2. `PCM Process`
	* sample the analog signal at regular intervals - `44100 Hz/ any other`
	* quantize the amplitude of the signal
	* encode the resulting signal into a binary format.
		* that can be stored and transmitted as digital data

PCM data is a sequence of digital samples - represents the amplitude of a signal at a specific point.
Each sample is a specific number of bits - 8,16,24:
**bits per sample represent the quantization levels and therefore the resolution of PCM data**
8-bit - 256 levels
16-bit - 65536 levels

Encoded PCM data can be stored in a variety of file formats: mp3 wav pcm aiff.
`PCM representation is lossless`

3. Convert the encoded data into an array format
4. `DTW Process`
	* define the DTW function `[DONE]`
	* load the audio to be investigates | `ALT: use the array data from step(3) `


### Challenges:
1. Extracting sampling frequency direclty from audio using our function:
Remedy - Redefine Function