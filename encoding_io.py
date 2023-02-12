"""
Auto Login - local file IO
By Hyder Pang @ 2023-2-8

"""


import base64


class base64_io:
    def __init__(self, filepath='log'):
        self.filepath = filepath

    def encode_strings(self, strings):
        encoded_strings = []
        for string in strings:
            encoded_string = base64.b64encode(string.encode()).decode()
            encoded_strings.append(encoded_string)
        return encoded_strings

    def decode_strings(self, encoded_strings):
        decoded_strings = []
        for encoded_string in encoded_strings:
            decoded_string = base64.b64decode(encoded_string.encode()).decode()
            decoded_strings.append(decoded_string)
        return decoded_strings

    def write_to_file(self, strings, file_path=None):
        if file_path == None:
            file_path = self.filepath
        encoded_strings = self.encode_strings(strings)
        with open(file_path, 'w') as f:
            for encoded_string in encoded_strings:
                f.write(encoded_string + '\n')

    def read_from_file(self, file_path=None):
        if file_path == None:
            file_path = self.filepath
        with open(file_path, 'r') as f:
            lines = f.readlines()
        encoded_strings = [line.strip() for line in lines]
        decoded_strings = self.decode_strings(encoded_strings)
        return decoded_strings