# busybox httpd -f -p 8080 -h /home/user/Music/wav_dir
import machine
import network
import time
import ustruct
import socket
import io

def connect_to_wifi():
    # Your network credentials
    ssid = 'your_ssid'
    password = 'your_password'
    #Connect to Wi-Fi
    wlan = network.WLAN(network.STA_IF)
    wlan.ifconfig(('your_static_ip', '255.255.255.0', '192.168.0.1', '205.171.3.25')) # put your static IP here
    time.sleep_ms(1000)
    wlan.active(True)
    time.sleep_ms(1000)
    wlan.connect(ssid, password)

    # Wait for connection to establish
    max_wait = 10
    while max_wait > 0:
        if wlan.isconnected():
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
    
    # Manage connection errors
    if wlan.isconnected():
        print('connected')
        return True
    else:
        print(wlan.status())
        return False

# these pins for ESP32C3
def init_i2s(rate=44100, bits=8, format=machine.I2S.MONO):
    return machine.I2S(
        0,
        sck    = machine.Pin(8),  # BCLK
        ws     = machine.Pin(9),  # LRC
        sd     = machine.Pin(10), # DIN
        mode   = machine.I2S.TX,
        bits   = bits,
        format = format,
        rate   = rate,
        ibuf   = 2048 )

def read_wav_header(first_44bytes):
    header = io.BytesIO(first_44bytes).read(44)
    riff, size, wave = ustruct.unpack('<4sI4s', header[0:12])
    if riff != b'RIFF' or wave != b'WAVE':
        raise ValueError("Not a valid WAV file")
    
    audio_format, num_channels, sample_rate = ustruct.unpack('<HHI', header[20:28])
    byte_rate, block_align, bits_per_sample = ustruct.unpack('<IHH', header[28:36])
    
    if (num_channels == 1):
        i2s = init_i2s(rate=sample_rate, bits=bits_per_sample, format=machine.I2S.MONO)
    else:
        i2s = init_i2s(rate=sample_rate, bits=bits_per_sample, format=machine.I2S.STEREO)
    return i2s

def play_wav(wav_name):
    header_done = False
    # Configuration
    HOST = 'your_host_ip'
    PORT = 8080            # your http port
    PATH = "/" + wav_name

    addr = socket.getaddrinfo(HOST, PORT)[0][-1]
    s = socket.socket()
    s.connect(addr)
    request = b"GET %s HTTP/1.0\r\nHost: %s\r\n\r\n" % (PATH.encode(), HOST.encode())
    s.sendall(request)
    while True:
        line = s.readline()
        if not line or line == b'\r\n': # this strips the http header
            break
    while True:
        if (not header_done):
            i2s = read_wav_header(s.recv(44)) # wav header
            header_done = True
        else:    
            data = s.recv(1024) # wav audio
            if data:            # not empty
                i2s.write(data)
            else:
                break
    s.close()
                
connect_to_wifi()
play_wav('stand_and_deliver.wav')