from flask import (make_response, current_app, Blueprint, jsonify, request, render_template)
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

@translator.route("/quiz")
def quiz():
    return render_template('quiz.html', title='Quiz')

@translator.route("/quiz_check_answer", methods=['GET', 'POST'])
def quiz_check_answer():
    data = request.json
    input_text = current_app.translator.get_input_text_from_request(data)
    response_text = current_app.translator.translate(input_text)
    response = {"text": response_text}
    res = make_response(jsonify(response))
    res.headers['Access-Control-Allow-Origin'] = '*'
    # HERE NOW I SCHOULD CHANGE THIS FUNction and adjust it ot quiz schema, i can use just response no need for server send events imo
    return res


@translator.route("/sample_data")
def sample_data():
    response = [{
        1:"nice",
        2:"bad"
    }]
    data = {
        "response": response
    }
    return jsonify(data)