
from google.cloud import translate_v2 as translate
import six

class Translator:

    def __init__(self):
        self.rasa_parser_url = 'http://localhost:5005/model/parse'
        self.translate_client = translate.Client()

    def translate(self, text, language="de"):
        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')
        result = self.translate_client.translate(
            text, target_language=language)
        return result['translatedText']
