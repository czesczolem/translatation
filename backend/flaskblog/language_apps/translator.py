from google.cloud import translate_v2 as translate
from .baseparser import BaseParser


class Translator(BaseParser):

    def __init__(self):
        BaseParser.__init__(self)
        self.translate_client = translate.Client()

    def handle_response(self, question, answer):
        print(f"RESP HANDLING current: {self.current_question}, question: {question}, answer: {answer}")
        if answer.strip() == self.current_question['en'].strip():
            print("answer is correct!")
            self.prep_question()
            return self.current_question

    def translate(self, text, language="de"):
        result = self.translate_client.translate(
            text, target_language=language)
        return result['translatedText']
