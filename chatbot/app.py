from flask import Flask, request, make_response, jsonify, render_template
from flask_cors import CORS
from google.cloud import translate_v2 as translate
import six
import requests
import json
from elasticsearch import Elasticsearch
from utils import Elasticsearcher
from datetime import datetime
import time
import collections



rasa_parser_url = 'http://localhost:5005/model/parse'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

translate_client = translate.Client()

app = Flask(__name__)
CORS(app)

index = 'translations'
# es = Elasticsearch()
# esr = Elasticsearcher(es, index)

conv_tracker = collections.deque([None] * 4, maxlen=4)




def get_intent(text):
    print(f"Getting intent from: {text}")
    data = {
        "text": text
    }
    # r = requests.post(rasa_parser_url, data=json.dumps(data), headers=headers)
    # rasa_response = json.loads(r.content)
    # print(rasa_response)
    # detected_intent = rasa_response['intent']['name']
    detected_intent = 'translate'
    return detected_intent

def translate(text, language="de"):
    result = translate_client.translate(
        text, target_language=language)
    return result['translatedText']

def break_string_after(x, split_factor):
    ind = x.find(split_factor) + len(split_factor) + 1
    return x[ind:]

def intent_handler(text_input, intent):
    if intent == "translate":
        text_to_translate = break_string_after(text_input, "translate")
        result_text = translate(text_to_translate, language="en")
    elif intent == "quiz":
        return ""
    else:
        result_text = "I dont know this intent..."
        result_text = translate(text_input, language="en")
    return result_text

def get_input_text_from_request(request):
    data = request.json
    text_input = data['answer']
    if isinstance(text_input, six.binary_type):
        text_input = text_input.decode('utf-8')
    return text_input

# def save_translation(text_input, intent, response_text):
#     conversation_unit = {
#             "date": datetime.today(),
#             "text_query": text_input,
#             "intent": intent if intent else "default",
#             "response": response_text,
#         }
#
#     conv_tracker.append(conversation_unit)
#     conv_id = int(time.time())
#
#     print(f"push data to elastic: {conversation_unit}")
#     res = es.index(index='translations', id=conv_id, body=conversation_unit)

def results():
    text_input = get_input_text_from_request(request)
    intent = get_intent(text_input)
    response_text = intent_handler(text_input, intent)
    # save_translation(text_input, intent, response_text)
    response = {"text": response_text}
    return response

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    res = make_response(jsonify(results()))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/parse_data', methods=['GET', 'POST'])
def parse_data():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        return make_response(jsonify({"status": "ok"}))

# run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)