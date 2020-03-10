import json
import os
from datetime import datetime

class JsonWriter:
    
    #TODO: refatorar esse método
    @staticmethod
    def write_json(json_content : list, result_file_path=None):
        # if result_file_path == None:
            
        #     file_name = now.strftime("jedi-result.json")

        #     result_file_path = os.path.join("../results", file_name)


        with open('/home/eduardol/UFLA/tcc/ArchPython/results/jedi-result.json', 'w') as out:
            json.dump(json_content , out)



