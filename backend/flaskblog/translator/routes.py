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
    question, answer = current_app.translator.handle_quiz_request(data)
    print(f"request data: {data}. question: {question}, answer: {answer}")

    if question == 1:
        current_app.translator.start_quiz()
        next_question_if_correct = current_app.translator.current_question
    else:
        next_question_if_correct = current_app.translator.handle_response(question, answer)
        print(next_question_if_correct)


    response = {
        "answer_correct": 1 if next_question_if_correct else 0,
        "next_question": next_question_if_correct['pl'] if next_question_if_correct else 0

    }
    print(f"response: {response}")


    res = make_response(jsonify(response))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


