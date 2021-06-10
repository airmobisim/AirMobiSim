import json
class Jsonparser:
    first = 0
    second = 0
    answer = 0
      
    # parameterized constructor
    def __init__(self, filename):
        self._filename = filename


    def readConfig(self):
        with open(self._filename) as json_file:
            return json.load(json_file)
