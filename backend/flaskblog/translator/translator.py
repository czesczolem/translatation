from google.cloud import translate_v2 as translate
import six

class Translator:

    def __init__(self):
        self.rasa_parser_url = 'http://localhost:5005/model/parse'
        self.translate_client = translate.Client()

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
