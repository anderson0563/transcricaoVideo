import speech_recognition as sr
import os
import math
from speech_recognition.recognizers import google, whisper
from os import walk
from pydub import AudioSegment

class SplitWavAudioMubin():
    def __init__(self, filename):
        self.filename = filename        
        self.audio = AudioSegment.from_wav(self.filename)
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(split_filename, format="wav")
        
    def multiple_split(self, min_per_split):
        total_mins = math.ceil(self.get_duration() / 60)
        for i in range(0, total_mins, min_per_split):
            split_fn = "./audio/" + str(i) + '_' + self.filename
            self.single_split(i, i+min_per_split, split_fn)
            print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splited successfully')

# Load the video file
video = AudioSegment.from_file("exame.mp4", format="mp4")
audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
audio.export("audio.wav", format="wav")
os.makedirs("./audio/")

file = "audio.wav"
split_wav = SplitWavAudioMubin(file)
split_wav.multiple_split(min_per_split=1)

filenames = next(walk("./audio/"), (None, None, []))[2]  # [] if no file

for file in filenames:
    if(len(file)==len("8_audio.wav")):
        os.rename("./audio/"+file, "./audio/"+"00"+file)
    if(len(file)==len("18_audio.wav")):
        os.rename("./audio/"+file, "./audio/"+"0"+file)

filenames = next(walk("./audio/"), (None, None, []))[2]  # [] if no file

filenames.sort()

r = sr.Recognizer()

file1 = open("transcricao.txt", 'w')

for file in filenames:
    with sr.AudioFile("./audio/" + file) as source:
        print(file)
        audio = r.record(source)
        s = r.recognize_google(audio, language = 'pt-BR')
        file1.writelines(s)

file1.close()