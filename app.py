from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from google.cloud import translate_v2 as translate
import six
import requests
import json


rasa_parser_url = 'http://localhost:5005/model/parse'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

translate_client = translate.Client()
app = Flask(__name__)


CORS(app)


@app.route('/')
def index():
    return 'Hello World!'

def get_intent(text):
    r = requests.post(rasa_parser_url, data=json.dumps(text), headers=headers)
    rasa_response = json.loads(r.content)
    detected_intent = rasa_response['intent']['name']
    return detected_intent

def translate(text, language="de"):
    result = translate_client.translate(
        text, target_language=language)
    return result['translatedText']


def intent_handler(text_input, intent):
    if intent == "translate":
        result_text = translate(text_input, language="de")
    else:
        result_text = "I dont know this intent..."
    return result_text

def get_input_text_from_request(request):
    data = request.json
    text_input = data['answer']
    if isinstance(text_input, six.binary_type):
        text_input = text_input.decode('utf-8')
    return text_input


def results():
    text_input = get_input_text_from_request(request)
    intent = get_intent(text_input)
    response_text = intent_handler(text_input, intent)
    response = {"text": response_text}
    return response


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    res = make_response(jsonify(results()))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

# run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)