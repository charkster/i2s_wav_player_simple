from machine import I2S
from machine import Pin
import ustruct

# select the pins that your MCU board supports
def init_i2s(rate=44100, bits=8, format=I2S.MONO):
    return I2S(
        0,     # MCU I2S channel num
        sck    = Pin(8),  # BCLK MAX98357A
        ws     = Pin(9),  # LRC  MAX98357A
        sd     = Pin(10), # DIN  MAX98357A
        mode   = I2S.TX,
        bits   = bits,
        format = format,
        rate   = rate,
        ibuf   = 2048 )

def read_wav_header(file):
    header = file.read(44)
    riff, size, wave = ustruct.unpack('<4sI4s', header[0:12])
    if riff != b'RIFF' or wave != b'WAVE':
        raise ValueError("Not a valid WAV file")
    
    audio_format, num_channels, sample_rate = ustruct.unpack('<HHI', header[20:28])
    byte_rate, block_align, bits_per_sample = ustruct.unpack('<IHH', header[28:36])
    
    if (num_channels == 1):
        i2s = init_i2s(rate=sample_rate, bits=bits_per_sample, format=I2S.MONO)
    else:
        i2s = init_i2s(rate=sample_rate, bits=bits_per_sample, format=I2S.STEREO)
    return i2s

def play_wav(filename):
    with open(filename, "rb") as f:
#        file.read(44) # skip header, replace read_wav_header instance with init_i2s instance
        i2s = read_wav_header(f)
        while True:
            data = f.read(1024)
            if not data:
                break
            i2s.write(data)

play_wav("music-16k-16bits-mono.wav")
