from flask import (make_response, current_app, Blueprint, jsonify, request)
from flask_login import current_user
from flaskblog import db

translator = Blueprint('translator', __name__)


@translator.route("/translate", methods=['GET', 'POST'])
def translate():
    data = request.json
    input_text = current_app.translator.get_input_text_from_request(data)
    response_text = current_app.translator.translate(input_text)
    response = {"text": response_text}
    res = make_response(jsonify(response))
    res.headers['Access-Control-Allow-Origin'] = '*'

    return res
