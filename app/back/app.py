import sys
import os
import wave
import json

import jinja2
from flask import Flask, request, redirect, make_response, jsonify
from vosk import Model, KaldiRecognizer, SetLogLevel
from nlp import extract_travel_info
from icecream import ic

from graph_exploration.exploration import convert_city_to_stop_points, load_graph, graph_exploration, convert_route_to_cities
from graph_exploration.utils import get_shortest_route

ALLOWED_EXTENSIONS = {'wav'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./"
os.environ["PYTHONIOENCODING"] = "utf-8"
SetLogLevel(-1)
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True
)
template = jinja_env.get_template("index.html")
audio_file_path = './audio_files'


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def index():
    return template.render(
        step1=True,
        step2=False,
        step3=False
    )

@app.route("/", methods=["POST"])
def speech_to_text():
    if request.method == "POST":
        print("FORM DATA RECEIVED")
        f = request.files['file']
        f.save(f.filename)

    sentences = 'Voyager en train de lille à lyon Les trains sont mieux. ' \
                'J\'irai de Lille à Lyon A toulon et prendre un bus à marseille. ' \
                'A toulon et prendre un avion à marseille. ' \
                'A toulon et marcher à marseille. ' \
                'Manger des fruits Nager a la plage.'
    return template.render(
        name= f.filename,
        text=sentences,
        step1=False,
        step2=True,
        step3=False
    )  # tester

    ic(request.form.get("toFile"))
    if request.form.get("toFile") == "on":
        file_path = os.path.join(audio_file_path, request.form.get("audio_file"))
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
        print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit(1)

    wf = wave.open(file_path, "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit(1)

    model = Model(model_path)
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
    if request.form.get("sentences") is None:
        make_response(jsonify(
                success=False,
                message="You need to provide sentences to determine the travel request"),
            400)

    # sentences = json.loads(request.form.get("sentences")).split('.')

    text_file = open("speech.txt", "r")
    sentences = text_file.read()
    text_file.close()

    ic(sentences.split('.'))
    result = extract_travel_info(sentences.split('.'))

    if result == False:
        make_response(jsonify(
                success=False,
                message="There was no valid travel request detected"),
            400)

    return template.render(
        cities=result,
        step2=False,
        step3=True
    )

    make_response(jsonify(
        success=True,
        result=result),
        200)


@app.route("/pathfinder", methods=["POST"])
def pathfinder():
    if request.form.get('origin') is None or request.form.get('dest') is None:
        make_response(jsonify(
                success=False,
                message="You need to post cities to find the shortest path. "),
            400)

    origin = convert_city_to_stop_points(request.form.get('departure'))
    dest = convert_city_to_stop_points(request.form.get('destination'))
    if len(origin) < 1 and len(dest) < 1:
        result = "Trajet Impossible"
    else:
        origin = origin[0]
        dest = dest[0]

        graph = load_graph()
        routes = graph_exploration(graph, origin, dest)
        route = get_shortest_route(routes)
        result = "{} en {}".format(" -> ".join(convert_route_to_cities(route)), route["duration"])
    return template.render(
    journey=result,
    step2=False,
    step3=True
    )

app.run(host="0.0.0.0", port="5000", debug=True)
