from .baseparser import BaseParser
import pandas as pd
import random
import json

def gab_data(data):
    prep_data = []
    for s in data:
        s = list(s)
        random_num = random.randint(0,2)
        answer = s[random_num]
        s.remove(answer)
        prep_data.append({
            "question": [s[0], s[1], "_ " * len(answer)],
            "answer":answer
        })
    return prep_data

def format_question(question):
    if type(question) == str:
        return question
    elif type(question) == list:
        resp = ''
        for x in question:
            resp += f"""<div class="col-sm-4"><div class="card"><div class="card-body"><h5 class="card-title">{x}</h5></div></div></div>"""
        return resp
    else:
        return ''

class Quiz(BaseParser):

    def __init__(self, dataloader):
        BaseParser.__init__(self)
        self.question_counter = 0
#         self.sample_data = [{"en": "good", "pl": "dobrze"}, {"en": "bad", "pl": "źle"}, {"en": "better", "pl": "lepiej"}]
        self.sample_data = gab_data(dataloader.data)
        self.current_question = self.sample_data.pop()

    def prep_question(self):
        try:
            self.current_question = self.sample_data.pop()
        except:
            self.current_question = {"en": "Quiz finished", "pl": "Quiz ukończony"}

    def handle_response(self, question, answer):
        print(f"RESP HANDLING current: {self.current_question}, question: {question}, answer: {answer}")
        if answer.lower().strip() == self.current_question['answer'].lower().strip():
            print("answer is correct!")
            self.prep_question()
            return self.current_question

    def handle_quiz_request(self, data):
        question = data['question']
        answer = data['answer']
        return question, answer