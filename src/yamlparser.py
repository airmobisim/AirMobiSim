import yaml
from yaml.loader import FullLoader

class Yamlparser:
    first = 0
    second = 0
    answer = 0
      
    # parameterized constructor
    def __init__(self, filename):
        self._filename = filename


    def readConfig(self):
        with open(self._filename) as yaml_file:
            return yaml.load(yaml_file, Loader=FullLoader)
