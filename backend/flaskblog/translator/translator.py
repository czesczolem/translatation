from google.cloud import translate_v2 as translate
import six

class Translator:

    def __init__(self):
        self.rasa_parser_url = 'http://localhost:5005/model/parse'
        self.translate_client = translate.Client()

    def start_quiz(self):
        self.question_counter = 0
        self.sample_data = [{"en": "good", "pl": "dobrze"}, {"en": "bad", "pl": "źle"}, {"en": "better", "pl": "lepiej"}]
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
        # if isinstance(question, six.binary_type):
        #     question = question.decode('utf-8').strip()
        # if isinstance(answer, six.binary_type):
        #     answer = answer.decode('utf-8').strip()
        return question, answer


    def get_input_text_from_request(self, data):
        text_input = data['answer']
        if isinstance(text_input, six.binary_type):
            text_input = text_input.decode('utf-8')
        return text_input

    def translate(self, text, language="de"):
        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')
        result = self.translate_client.translate(
            text, target_language=language)
        return result['translatedText']
