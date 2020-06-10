from .baseparser import BaseParser
import pandas as pd



class Quiz(BaseParser):

    def start_quiz(self):
        self.question_counter = 0
        # self.sample_data = [{"en": "good", "pl": "dobrze"}, {"en": "bad", "pl": "źle"}, {"en": "better", "pl": "lepiej"}]
        self.sample_data = pd.read_csv('test_verbs.py')
        self.current_question = self.sample_data.pop()

    def prep_question(self):
        try:
            self.current_question = self.sample_data.pop()
        except:
            self.current_question = {"en": "Quiz finished", "pl": "Quiz ukończony"}

    def handle_response(self, question, answer):
        print(f"RESP HANDLING current: {self.current_question}, question: {question}, answer: {answer}")
        if answer.strip() == self.current_question['en'].strip():
            print("answer is correct!")
            self.prep_question()
            return self.current_question

    def handle_quiz_request(self, data):
        question = data['question']
        answer = data['answer']
        return question, answer
