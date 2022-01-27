import sys
import os
import wave
import json

import jinja2
from flask import Flask, request, redirect, make_response, jsonify
from vosk import Model, KaldiRecognizer, SetLogLevel
from nlp import extract_travel_request
from icecream import ic

ALLOWED_EXTENSIONS = {'wav'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./uploaded/"
os.environ["PYTHONIOENCODING"] = "utf-8"
SetLogLevel(-1)
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True
)
template = jinja_env.get_template("index.html")



def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    return template.render(
        step2=False,
        step3=False
    )

@app.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    sentences = [
        'Voyager en train de lille à lyon',
        'Les trains sont mieux. J\'irai de Lille à Lyon',
        'A toulon et prendre un bus à marseille',
        'A toulon et prendre un avion à marseille',
        'A toulon et marcher à marseille',
        'Manger des fruits',
        'Nager a la plage'
    ]
    return template.render(
        text=sentences,
        step2=True,
        step3=False
    )  # tester
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
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result.append(json.loads(rec.Result()))
    ret = [sentence["alternatives"][0]["text"] for sentence in result]
    print(ret)
    # TODO: remplacer sentences en dessous avec le resultat
    # return template.render(
    #     text=sentences,
    #     step2=True,
    #     step3=False
    # )

    return json.dumps(ret)


@app.route("/travel-request", methods=["GET", "POST"])
def travel_request():
    return template.render(
        cities="Paris, Lyon",
        step2=True,
        step3=True
    )
    if request.form.get("sentences") is None:
        make_response(jsonify(
                success=False,
                message="You need to provide sentences to determine the travel request"),
            400)

    ic(request.form.get("sentences"))
    result = extract_travel_request(json.loads(request.form.get("sentences")))

    if result == False:
        make_response(jsonify(
                success=False,
                message="There was no valid travel request detected"),
            400)

    make_response(jsonify(
            success=True,
            result=result),
        200)

    return template.render(
        cities=result,
        step2=True,
        step3=True
    )


@app.route("/pathfinder", methods=["POST"])
def pathfinder():
    return template.render(
        journey="Paris to Lyon on Line 5",
        step2=True,
        step3=True
    )
    if request.form.get("cities") is None:
        make_response(jsonify(
                success=False,
                message="You need to post cities to find the shortest path. "),
            400)
    cities = json.loads(request.form.get("cities"))
    pass

app.run(host="0.0.0.0", port="5000", debug=True)