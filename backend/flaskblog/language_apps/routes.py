from flask import (make_response, current_app, Blueprint, jsonify, request, render_template)
from flask_login import current_user
from flaskblog import db
from .quiz import format_question

language_apps = Blueprint('language_apps', __name__)


@language_apps.route("/translate", methods=['GET', 'POST'])
def translate():
    data = request.json
    input_text = current_app.translator.get_input_text_from_request(data)
    response_text = current_app.translator.translate(input_text)
    response = {"text": response_text}
    res = make_response(jsonify(response))
    res.headers['Access-Control-Allow-Origin'] = '*'

    return res


####

@language_apps.route("/quiz")
def quiz():
    return render_template('quiz.html', title='Quiz')

@language_apps.route("/quiz_check_answer", methods=['GET', 'POST'])
def quiz_check_answer():
    data = request.json
    question, answer = current_app.quiz.handle_quiz_request(data)
    print(f"request data: {data}. question: {question}, answer: {answer}")

    if question == 1:
        current_app.quiz.start_quiz()
        next_question_if_correct = current_app.quiz.current_question
    else:
        next_question_if_correct = current_app.quiz.handle_response(question, answer)
    print(next_question_if_correct)


    response = {
        "answer_correct": 1 if next_question_if_correct else 0,
        "next_question": format_question(next_question_if_correct['question']) if next_question_if_correct else 0

    }
    print(f"response: {response}")


    res = make_response(jsonify(response))
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

###

@language_apps.route("/brain")
def brain():
    return render_template('brain.html', title='Brain')

@language_apps.route("/brain_test", methods=['GET', 'POST'])
def brain_test():
    data = request.json
    input_text = current_app.translator.get_input_text_from_request(data)
    deps_graph = current_app.brain.process_deps(input_text)
    response = {"text": str(deps_graph)}
    res = make_response(jsonify(response))
    res.headers['Access-Control-Allow-Origin'] = '*'

    return res

