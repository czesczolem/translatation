from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from google.cloud import translate_v2 as translate
import six
import requests
import json
from elasticsearch import Elasticsearch
from utils import Elasticsearcher
from datetime import datetime
import time



rasa_parser_url = 'http://localhost:5005/model/parse'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

translate_client = translate.Client()

app = Flask(__name__)
CORS(app)

index = 'translations'
es = Elasticsearch()
esr = Elasticsearcher(es, index)

intents_tracker = []

@app.route('/')
def index():
    return 'Hello World!'

def get_intent(text):
    print(f"Getting intent from: {text}")
    data = {
        "text": text
    }
    r = requests.post(rasa_parser_url, data=json.dumps(data), headers=headers)
    rasa_response = json.loads(r.content)
    print(rasa_response)
    detected_intent = rasa_response['intent']['name']
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
    return result_text

def get_input_text_from_request(request):
    data = request.json
    text_input = data['answer']
    if isinstance(text_input, six.binary_type):
        text_input = text_input.decode('utf-8')
    return text_input

def save_translation(text_input, intent, response_text):
    conversation_data = {
            "date": datetime.today(),
            "text_query": text_input,
            "intent": intent,
            "response": response_text,
            "intents_tracker": intents_tracker
        }
    intents_tracker.append(intent)
    conv_id = int(time.time())
    print(f"push data to elastic: {conversation_data}")
    res = es.index(index='translations', id=conv_id, body=conversation_data)

def results():
    text_input = get_input_text_from_request(request)
    intent = get_intent(text_input)
    response_text = intent_handler(text_input, intent)
    save_translation(text_input, intent, response_text)
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