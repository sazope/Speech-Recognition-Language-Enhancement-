#the os module that provides a portable way of using operating system-dependent functionality
import os
#imports the sounddevice module and aliases it to sd.
import sounddevice as sd
#imports the write function from the scipy.io.wavfile module. 
# This function is used to write audio data to a WAV file.
from scipy.io.wavfile import write
# This line imports the Flask class, render_template function, and request object from the flask module. 
# Flask is a micro web framework for building web applications in Python.
from flask import Flask, render_template, request
# imports the openai module, which provides a Python interface for interacting with OpenAI's GPT-3 language model.
import openai
#imports the whisper module, which provides a Python interface for interacting with OpenAI's Whisper automatic speech recognition (ASR) system.
import whisper
#This line sets the OpenAI API key, which is used to authenticate requests to the OpenAI API.
openai.api_key = "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"
#This line loads the Whisper ASR model.
model = whisper.load_model("base")
#This line creates a new Flask web application instance.
app = Flask(__name__)

#  This line defines a new function named record that takes a single argument, duration
def record(duration):
#This line sets the sample rate of the audio recording to 44.1 kHz
    fs = 44100
#This line sets the number of audio channels to 1 (mono)
    channels = 1
#This line records audio for the specified duration (in seconds) using the sounddevice module and stores the audio data in the myrecording variable.
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
# This line prints a message to the console indicating that audio recording is in progress.
    print("Recording Audio - Speak now!")
#This line waits until the audio recording is complete.
    sd.wait()
#This line prints a message to the console indicating that audio recording is complete.
    print("Audio recording complete")
#This line writes the audio data to a WAV file named output.wav
    write('output.wav', fs, myrecording)

#This line defines a new function named `audio_check
def audio_check(path):
#This line defines a new function named home that returns the rendered template for the index.html file.
    result = model.transcribe(path)

    return result["text"]
# This line creates a new route for the Flask web application that maps to the root URL (/)
@app.route('/')
#This line defines a new function named home that returns the rendered template for the index.html file
def home():
    return render_template('index.html')
'''This line creates a new route for the Flask web application that maps to the /transcribe 
URL and specifies that the route only accepts HTTP POST requests'''
@app.route('/transcribe', methods=['POST'])
# This line defines a new function named transcribe
def transcribe():
#This line sets the path to the audio file that will be transcribed
    path = "output.wav"
#This line calls the record function to record audio for 5 seconds
    record(5)
#This line calls the audio_check function to transcribe the audio file and store the transcribed text in the text variable
    text = audio_check(path)
#This line returns the rendered template for the result.html file with the transcribed text as a variable.
    return render_template('result.html', text=text)
#This line checks if the script is being run directly (as opposed to being imported as a module)
if __name__ == '__main__':
#This line starts the Flask web application and runs it in debug mode
    app.run(debug=True, port=8000)
