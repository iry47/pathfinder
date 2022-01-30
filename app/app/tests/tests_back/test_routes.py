import os
import wave
import json
import unittest
from icecream import ic

from flask import Flask, request, redirect, make_response, jsonify
from vosk import Model, KaldiRecognizer, SetLogLevel
from app.app import allowed_file

class TextExtractTests(unittest.TestCase):

    """class for running unittests."""

    def setUp(self):
        """Your setUp"""
        self.audio_file_path = './audio_files'

    def test_speech_to_text(self):
        ic(request.form.get("toFile"))
        if request.form.get("toFile") == "on":
            file_path = os.path.join(self.audio_file_path, request.form.get("audio_file"))
        else:
            uploaded_file = request.files["file"]
            if uploaded_file and allowed_file(uploaded_file.filename):
                filename = uploaded_file.filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                uploaded_file.save(file_path)

        ic(file_path)

        # model_name = "small"
        model_name = "linto"

        model_path = "./models/{}".format(model_name)

        if not os.path.exists(model_path):
            print(
                "Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
            exit(1)

        wf = wave.open(file_path, "rb")

        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print("Audio file must be WAV format mono PCM.")
            exit(1)

        model = Model(model_path)
        rec = KaldiRecognizer(model, wf.getframerate())
        # rec.SetMaxAlternatives(10)
        rec.SetWords(True)

        result = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result.append(json.loads(rec.Result()))
        ret = [sentence["alternatives"][0]["text"] for sentence in result]
        print(ret)