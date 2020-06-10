import six


class BaseParser:

    def __init__(self):
        self.rasa_parser_url = 'http://localhost:5005/model/parse'

    def get_input_text_from_request(self, data):
        text_input = data['answer']
        if isinstance(text_input, six.binary_type):
            text_input = text_input.decode('utf-8')
        return text_input
