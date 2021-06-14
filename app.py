from re import split
from flask import Flask,render_template,request 
from flask_bootstrap import Bootstrap
import test
import videoTester
import voiceAnalyzer
import time
import pyaudio
import os
import wave
app = Flask(__name__)
Bootstrap(app)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def inde():
    return render_template("index.html")

@app.route('/qstn')
def phq():
    return render_template("phq9.html",data="Anxiety and Depression Detection")

@app.route('/expression') 
def expression():
    p=videoTester.exp()
    return render_template("face.html",data=p)


@app.route('/face') 
def face():
    return render_template("face.html",data = "Anxiety and Depression Detection")

@app.route('/voice')
def voice():
    return render_template("voice.html",data = "Click on the Mic to Record")

@app.route('/voice_recording')
def voice_recording():
    CHUNK = 1024 
    FORMAT = pyaudio.paInt16 #paInt8
    CHANNELS = 2 
    RATE = 44100 #sample rate
    RECORD_SECONDS = 4
    WAVE_OUTPUT_FILENAME = "output10.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK) #buffer

    #return render_template("voice.html", data = "Recording ....")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data) # 2 bytes(16 bits) per channel

    

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return render_template("voice.html", data = "Done recording.")

@app.route('/voice_analyzer')
def voice_analyzeer():
    res = voiceAnalyzer.alalyzer()
    res2 = os.system('python test.py -f output10.wav > output.txt')
    file =  open("output.txt","r")
    #gender = ["male","female"]
    for line in file:
        if "Result:" in line:
            sound = line.split()
            res2 = sound[1]
            
            
    
    return render_template("voice.html",data = res)



    