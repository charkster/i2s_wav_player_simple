# i2s_wav_player_simple

A minimal Micropython script for playing a WAV file using I2S with an ESP32C3 and MAX98357A.

Lots of sample WAV files can be found [here](https://github.com/miketeachman/micropython-i2s-examples/tree/master/wav).

Also added [i2s_wav_file_from_http_get.py](https://github.com/charkster/i2s_wav_player_simple/blob/main/i2s_wav_file_from_http_get.py) which gets the wav file from a http server (I used busybox). You can play a wav file of any size as data is read 1Kbyte at a time from the http server. I may experiment with lighttpd to see if I can have the http server convert from mp3 to wav on-the-fly.

![picture](https://github.com/charkster/i2s_wav_player_simple/blob/main/esp32c3_xiao_max98357a.png)
