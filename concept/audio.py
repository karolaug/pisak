#!/usr/bin/python3
#Note: Indented using tabs
import pyaudio
import wave
 
class AudioFile:
    chunk = 1024
 
    def __init__(self, file):
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )
 
    def play(self):
        data = self.wf.readframes(self.chunk)
        while data != '':
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)
 
    def close(self):
        self.stream.close()
        self.p.terminate()

