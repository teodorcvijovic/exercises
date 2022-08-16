# Create configuration class that can be used to access configuration through
# attributes. Configuration data can be passed in yaml or json format.
# e.g config.a.b.c < = > config[‘a’][‘b’][‘c’] < = >
# config[‘a’].b.c < = > config.a[‘b.c’] < = > config[‘a.b.c’]
# Tips: try to implement __getattr__ and __getitem__ magic methods.

import argparse
import json
from dotmap import DotMap


# converts a dictionary to dotmap so fields are accessible via dot
class DotMapWrapper(DotMap):

    def __getitem__(self, key):
        if '.' in key:
            keys = key.split('.')
            obj = self
            for k in keys:
                obj = obj.get(k)
            return obj
        return self.get(key)

    def __getattr__(self, key):
        return self.__getitem__(key)


class Configuration:

    def __init__(self, json_file_name):
        try:
            file = open(json_file_name, 'r')
            json_string = file.read()
            file.close()
            self.obj = DotMapWrapper(json.loads(json_string))
        except json.decoder.JSONDecodeError:
            print('error: wrong format')
            exit(1)
        except FileNotFoundError:
            print('error: file does not exists')
            exit(1)

    def __getitem__(self, key):
        if '.' in key:
            keys = key.split('.')
            obj = self.obj
            for k in keys:
                obj = obj.get(k)
            return obj
        return self.obj.get(key)

    def __getattr__(self, key):
        return self.__getitem__(key)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='File should be in .json '
                                                   'format')
    args = parser.parse_args()

    conf_obj = Configuration(args.filename)

    # tests
    print(conf_obj['project.name'].lastname)
    print(conf_obj.project['name'].lastname)
    print(conf_obj.project['name.lastname'])
