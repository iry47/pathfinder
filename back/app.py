from vosk import Model, KaldiRecognizer, SetLogLevel 

import sys
import os


import wave
import json

from flask import Flask, request, redirect

ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./uploaded/" 

os.environ["PYTHONIOENCODING"] = "utf-8"

SetLogLevel(-1)

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.post("/speech_to_text")
def speech_to_text():
    uploaded_file = request.files["file"]
    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = uploaded_file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(file_path)

    model_name = "linto-model"

    path = "./models/{}".format(model_name)

    if not os.path.exists(path):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit(1)

    wf = wave.open(file_path, "rb")
    
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit(1)

    model = Model(path)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetMaxAlternatives(10)
    rec.SetWords(True)

    result = []
    partials = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result.append(json.loads(rec.Result()))
        else:
            partials.append(json.loads(rec.PartialResult()))

    ret = [sentence["alternatives"][0]["text"] for sentence in result]
    return json.dumps(ret)

