# Library to use PyAudio for audio input
# Feb 26, 2023 v0.02
# IoT for Kids: https://jxsboston.github.io/IoT-Kids/
#
# PyAudio's web page: https://people.csail.mit.edu/hubert/pyaudio/

import pyaudio, math, wave, numpy as np

audio = pyaudio.PyAudio()

# Default sampling rate: 44,100 (CD quality)
# Default # of channels: 1
# Default sound format: paInt16
# Default sample width in bytes: 2 (= FORMAT/8 = 16/8)
# Default FPG (frames per buffer): 4,410 (44,100/10)
SAMPLING_RATE = 44100
FORMAT = pyaudio.paInt16
SAMPLE_WIDTH = audio.get_sample_size(FORMAT)
CHANNELS = 1
FRAMES_PER_BUFFER = math.floor(SAMPLING_RATE/10)

# Function to initizalize PyAudio with the default settings
# and open a new audio stream for sound recording
#   Returns a new audio stream. 
#
def init(*, samplingRate = SAMPLING_RATE):
    global SAMPLING_RATE, FRAMES_PER_BUFFER
    SAMPLING_RATE = math.floor(samplingRate)
    FRAMES_PER_BUFFER = math.floor(SAMPLING_RATE/10)
    
    stream = audio.open(rate=SAMPLING_RATE,
                        format=FORMAT,
                        channels=CHANNELS,
                        frames_per_buffer=FRAMES_PER_BUFFER,                        
                        input=True)
    return stream

# Function to close an open stream and terminate the current PyAudio instance
#
def close(stream):
    stream.close()
    audio.terminate()

# Function to capture sound from the suplied stream. It captures
# and returns FRAMES_PER_BUFFER samples. By default, they are for
# 0.1 sec long sound beacuse 10 * FRAMES_PER_BUFFER = SAMPLING_RATE
# by default.
#     duration (float): Duration to capture sound in seconds
#     Returns a list (numpy.ndarray) of normalized [0.0,1.0] sound samples
#
def capture(stream, *, duration=0.1):
    sampleCountToCapture = math.floor(SAMPLING_RATE * duration)
    buffer = stream.read(sampleCountToCapture)
    return np.frombuffer(buffer, dtype=np.int16)/ float(2**(SAMPLE_WIDTH*8-1))


# Function to save sound wave samples as a WAV file.
#   samples (numpy.ndarray): A list of sound wave samples that are normalized in [0,1]
#   outputFileName (string): Name of the output WAV file
#
def saveSamplesAsWav(samples, outputFileName):
    if type(samples) is not np.ndarray:
        print("Provided sound wave samples are not in numpy.ndarray.")
    else:
        samples = samples * float(2**(SAMPLE_WIDTH*8-1))
        bSamples = samples.astype(np.int16).tobytes()
        bData = b""
        bData += bSamples
        w = wave.Wave_write(outputFileName)
        params = (CHANNELS, SAMPLE_WIDTH, SAMPLING_RATE, len(bData), "NONE", "not compressed")
        w.setparams(params)
        w.writeframes(bData)
        w.close()
