import json
import sys
import os
import wave

from vosk import Model, KaldiRecognizer
from icecream import ic

def get_transcription(file_path):
    # model_name = "small"
    model_name = "linto"

    model_path = "app/app/back/nlp/models/{}".format(model_name)
    # model_path = "./models/{}".format(model_name)

    if not os.path.exists(model_path):
        ic(model_path)
        print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit(1)

    wf = wave.open(file_path, "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit(1)

    ic(model_path)
    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    # rec.SetMaxAlternatives(10)
    # rec.SetWords(True)

    result = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result.append(json.loads(rec.Result()))
    ic(result)
    # ret = [sentence["alternatives"][0]["text"] for sentence in result]
    return result[0]["text"]