import os
import yaml
from pprint import pprint
from glob import glob

PARSERS = '../parsers'

def data_merge(obj_a, obj_b):
    """merges obj_b into obj_a and return merged result

    Args:
        obj_a (dict) The "merge into dict"
        obj_b (dict) The "merge from dict"

    Returns:
        dict:  The obj_a with obj_b added to it
    """
    key = None
    try:
        if obj_a is None or isinstance(obj_a, (str, unicode, int, long, float)):
            # border case for first run or if a is a primitive
            obj_a = obj_b
        elif isinstance(obj_a, list):
            # lists can be only appended
            if isinstance(obj_b, list):
                # merge lists
                obj_a.extend(obj_b)
            else:
                # append to list
                obj_a.append(obj_b)
        elif isinstance(obj_a, dict):
            # dicts must be merged
            if isinstance(obj_b, dict):
                for key in obj_b:
                    if key in obj_a:
                        obj_a[key] = data_merge(obj_a[key], obj_b[key])
                    else:
                        obj_a[key] = obj_b[key]
            else:
                raise 'Cannot merge non-dict "%s" into dict "%s"' % (obj_b, obj_a)
        else:
            raise 'NOT IMPLEMENTED "%s" into "%s"' % (obj_b, obj_a)
    except TypeError, exc:
        raise 'TypeError "%s" in key "%s" when merging "%s" into "%s"' % (exc, key, obj_b, obj_a)
    return obj_a


def load_parsers(os_name):
    """ Load the parsers for a devices OS, store in dict

    Args:
        devices (dict): A dict of devices
        args (namespace): The cli args

    Returns:
        dict: A dict of devices, each with parsers attached

    """
    models = []
    directory = '%s/%s' % (PARSERS, os_name)
    parser_files = [y for x in os.walk(directory)
                    for y in glob(os.path.join(x[0], '*.yml'))]

    for parser_file in parser_files:
        with open(parser_file, 'r') as stream:
            parsers = yaml.load(stream)
        for parser in parsers:
            this_model = {}
            this_model['model'] = {}
            for match in parser['matches']:
                this_model['name'] = match['name']
                for line in match['lines']:
                    this_model['model'] = data_merge(this_model['model'], line['path'])
                    if 'lines' in line:
                        for cline in line['lines']:
                            this_model['model'] = data_merge(this_model['model'], cline['path'])
            models.append(this_model)
            # device['parsers'].append(parser['path'])
    return models

models = load_parsers('cisco_ios-xe')

for model in models:
    print '### %s' %model['name']
    print '```yaml'
    print(yaml.safe_dump(model['model'], default_flow_style=False))
    print '```'
