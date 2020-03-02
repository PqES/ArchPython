import json
import glob

class InputReader:
    
    @staticmethod
    def get_json_content(file_path):
        with open(file_path) as input_file:
            return json.load(input_file)

