# Library to process and visualize sound samples
# Feb 26, 2023 v0.09
# IoT for Kids: https://jxsboston.github.io/IoT-Kids/

import pyaudio, wave, numpy as np, matplotlib.pyplot as plt
from scipy import signal
from math import pow, log2
from typing import Optional

# Function to draw a figure that plots sound samples over time. 
#   soundSamples (np.ndarray): Samples of a sound wave
#   duration (float): Duration of a sound
#   samplingRate (int): Sampling rate of a sound
#
def drawSoundSamples(*, soundSamples: np.ndarray,
                     duration: float, samplingRate: int,) -> None:
    plt.xlabel("Time (milliseconds)")
    plt.plot(
        np.arange(0, duration*1000, duration*1000/soundSamples.size),
        soundSamples)
    plt.show()

# Function to extract sound samples from a given WAV file.
#   wavFileName (str): File name (path) of the WAV file.
#
#   Returns an array (np.ndarray) of sound samples.
#
def wavToSamples(wavFileName: str) -> Optional[np.ndarray]:    
    wavFile = wave.open(wavFileName, mode="rb")
    # If the recorded sound is formatted in CD quality (with "-f cd"
    # option for the arecord command), sampwidth==2 (bytes), dtype=="int16". 
    print("Reading " + wavFileName + ": " + str(wavFile.getparams()))
    sampleWidth = wavFile.getsampwidth()
    if sampleWidth > 4:
        print("Unsupported bit depth (sample width): " + str(sampleWidth*8) +
              " bits. Returning None (0 samples).")
        return None
    # Get the number of sound samples in wavFile
    # Given the sampling rate of 4,4100fps (CD-quality sound)
    # and the sound duration of 3 seconds, total number of
    # samples (or frames) should be 132,300 (4,4100fps * 3sec).
    sampleCount = wavFile.getnframes()
    # Get sound samples as a "bytes" object
    samples = wavFile.readframes(sampleCount)
    wavFile.close()
    # Convert binary/hexadecimal samples (in bytes) to a numpy.ndarray
    # of int16/decimal samples
    # Normalize each sample value (each array element) to [0, 1]
    if sampleWidth == 1:
        # Unsigned 8 bits
        return np.frombuffer(samples, dtype="uint8") / float(2**(sampleWidth*8))
    elif sampleWidth == 2:
        # Signed 16 bits
        return np.frombuffer(samples, dtype="int16") / float(2**(sampleWidth*8-1))
    elif sampleWidth == 4:
        # Signed 32 bits
        return np.frombuffer(samples, dtype="float32") / float(2**(sampleWidth*8-1))

# Function to perform FFT for given sound samples
#   samples (np.ndarray): Sound samples.
#
#   Returns a frequency spectrum as an array (np.ndarray)
#
def fft(samples: np.ndarray) -> np.ndarray:
    # Do FFT and adjust/normalize the amplitude of each frequency
    f = np.fft.fft(samples) / (samples.size/2)
    # Convert comlex numbers to absolute values 
    fAbs = np.abs(f)
    #fAbs[0] = fAbs[0]/2
    # Ignore (put the amplitude of 0 to) the second half of freq spectrum
    # by considering the Nyquist frequency
    for i in range(int(samples.size/2)+1, samples.size):
        fAbs[i] = 0
    return fAbs

# Function to get the highest frequency component from a given freq spectrum
#   freqSpectrum (np.ndarray): Frequency spectrum
#   samplingRate (int): Sampling frequency
#
#   Returns the highest frequency component.
#
def getHighestPeakFrequency(*, freqSpectrum: np.ndarray, samplingRate: int)-> float:
    maxFreqIndex = np.argmax(freqSpectrum)
    freqAxis = np.linspace(0, samplingRate, freqSpectrum.size)
    return freqAxis[maxFreqIndex]

# Function to draw a frequency spectrum (sound wave amplitude as a
# function of frequency)
#   freqSpectrum (np.ndarray): Frequency spectrum
#   samplingRate (int): Sampling frequency
#
def drawFreqSpectrum(*, freqSpectrum: np.ndarray, samplingRate: int)-> None: 
    freqAxis = np.linspace(0, samplingRate, freqSpectrum.size)
    plt.xlabel("Frequency (Hz)")
    plt.axis([0, samplingRate/2, 0, max(freqSpectrum)*1.5])
    plt.plot(freqAxis, freqSpectrum)
    plt.show()

# Function to draw a frequency spectrum (sound wave amplitude as a
# function of frequency) with peak indicators (as red dots)
#   freqSpectrum (np.ndarray): Frequency spectrum
#   samplingRate (int): Sampling frequency
#   peakDetectionFilter (int): 
#
#
def drawPeakFreqSpectrum(*, freqSpectrum: np.ndarray, samplingRate: int,
                         peakDetectionFilter: int = 1) -> Optional[np.ndarray]: 
    peakFreqIndices = signal.argrelmax(freqSpectrum, order=peakDetectionFilter)
    freqAxis = np.linspace(0, samplingRate, freqSpectrum.size)

    plt.xlabel("Frequency (Hz)")
    plt.axis([0, samplingRate/2, 0, max(freqSpectrum)*1.5])
    plt.plot(freqAxis, freqSpectrum)
    plt.plot(freqAxis[peakFreqIndices], freqSpectrum[peakFreqIndices], "ro")
    plt.show()

    peaks = dict()
    for index in peakFreqIndices[0]:
        if index > samplingRate/2: break
        peaks[freqAxis[index]] = freqSpectrum[index]
    return peaks

# def getPeakFrequencies(*, freqSpectrum: np.ndarray, samplingRate: int, freqCount: int)-> float:
#     maxFreqIndices = np.argsort(freqSpectrum)
#     freqAxis = np.linspace(0, samplingRate, freqSpectrum.size)
#     freqs = list()
#     for index in maxFreqIndices[-freqCount : :]:
#         freqs.append(freqAxis[index])    
#     return freqs

A4 = 440
C0 = A4 * pow(2, -57/12)
noteNames =["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def freqToPitchLevel(freq):
    pitchLevel = log2( (freq/C0)**12 )
    return int( round(pitchLevel, 0) )

def freqToNoteName(freq):
    pitchLevel = freqToPitchLevel(freq)
    return pitchLevelToNoteName(pitchLevel)

def pitchLevelToNoteName(pitchLevel):
    octave = pitchLevel // 12
    noteId = pitchLevel % 12
    noteName = noteNames[noteId]
    return noteName + str(octave)
