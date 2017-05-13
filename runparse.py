""" Parses structured text into structured data_merge
"""

from __future__ import print_function
from collections import OrderedDict
from argparse import ArgumentParser, RawTextHelpFormatter
import re
import shutil
from shutil import copyfile
from glob import glob
import os
from os import listdir
from os.path import isfile, join
from pprint import pprint
import logging
import inspect
import ipaddress
import jinja2
import yaml

CONFIGURATIONS_DIR = './configurations'
HOST_VARS = './host_vars'
HOST_VARS_TEMP = './host_vars.tmp'
PARSERS = './parsers'
REMOVERS = './removers'
TEMPLATES = './templates'
LJUST = 70 #the msg width

def represents_int(string):
    """ Test if a string can be turned into an int

    Args:
        string (str): A string to Test

    Returns:
        bool: True if the string is an int
    """
    try:
        int(string)
        return True
    except ValueError:
        return False

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

def remove_keys(obj, rubbish):
    """ Removes keys from a dictionary

    Args:
        obj (dict): The dict from which the keys should be removed
        rubbish (list): A list of keys to removed

    Returns:
        dict:  The orginal dict with keys removed
    """


    if isinstance(obj, dict):
        obj = {
            key: remove_keys(value, rubbish)
            for key, value in obj.iteritems()
            if key not in rubbish}
    elif isinstance(obj, list):
        for entry in obj:
            if isinstance(entry, dict):
                entry = remove_keys(entry, rubbish)
            elif isinstance(entry, list):
                entry = [remove_keys(item, rubbish) for item in entry if item not in rubbish]
    return obj

def seq_in_seq(subseq, seq):
    """
    Args:
        subseq (list):
        seq (list):

    Returns:
        int: position of subseq on seq or -1.
    """
    idx, slen, blen = -1, len(seq), len(subseq)
    if blen == 0:
        return -1
    try:
        while True:
            idx = seq.index(subseq[0], idx + 1, slen - blen + 1)
            if subseq == seq[idx:idx + blen]:
                return idx
    except ValueError:
        return -1

def get_configurations():
    """ Load device configurations from the file system

    Returns:
        dict: A dict of devices with several keys
    """
    devices = []
    device_configs = [fname for fname in listdir(CONFIGURATIONS_DIR) \
                      if isfile(join(CONFIGURATIONS_DIR, fname))]
    for device_config in device_configs:
        hostname = '.'.join(device_config.split('.')[:-1])
        print_log(hostname, 'ljust')
        device = {}
        device['hostname'] = hostname
        device['failed'] = False
        with open('%s/%s' % (CONFIGURATIONS_DIR, device_config)) as cfile:
            config = cfile.read().splitlines()
        device['configuration'] = [item.rstrip() for item in config]
        device['working_configuration'] = device['configuration']
        devices.append(device)
        print_log('ok', 'ok')
    return devices

def copy_host_vars(devices, src_dir, dst_dir):
    """ Copy files between directories

    Args:
        devices (dict): A dictionary of devices for which files should be copied
        src_dir (str): The source directory
        dst_dir (str): The destination directory

    Returns:
        dict: The dict of devices, updated with failuers
    """
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for device in devices:
        if not device['failed']:
            print_log(device['hostname'], 'ljust')
            try:
                src = '%s/%s.yml' % (src_dir, device['hostname'])
                dst = '%s/%s.yml' % (dst_dir, device['hostname'])
                copyfile(src, dst)
                print_log('ok', 'ok')
            except IOError:
                device['failed'] = True
                reason = "host_vars file missing."
                device['failed_reason'] = reason
                print_log(reason, 'failed')
                break
    return devices

def load_host_vars(device):
    """ Load the host_vars file for a device

    Args:
        device (dict): A dict of a device

    Returns:
        dict: The devices with it's host_varss added
    """
    try:
        with open('%s/%s.yml' % (HOST_VARS_TEMP, device['hostname']), 'r') as stream:
            try:
                device.update(yaml.load(stream))
            except TypeError:
                device['failed'] = True
                device['failed_reason'] = "host_vars file appears empty."
            except yaml.YAMLError:
                device['failed'] = True
                device['failed_reason'] = "Failed host_vars import."
    except IOError:
        device['failed'] = True
        reason = "Missing host_vars file."
        device['failed_reason'] = reason
    return device

def get_os(devices):
    """ Ensure each device has an OS specified

    Args:
        devices (dict): A dict of devices

    Returns:
        dict: A dict of devices, flagged if no OS

    """
    for device in devices:
        if not device['failed']:
            print_log(device['hostname'], 'ljust')
            device = load_host_vars(device)
            if device['failed']:
                print_log(device['failed_reason'], 'failed')
                continue
            else:
                if not 'os' in device:
                    device['failed'] = True
                    reason = "host_vars missing OS for %s" % device['hostname']
                    device['failed_reason'] = reason
                    print_log(reason, 'failed')
                else:
                    print_log('ok', 'ok')
    return devices

def check_tags(parser, args):
    """ Compare cli tags to parser tags

    Args:
        parser (dict): The parser in question
        args (namepsace): The cli args

    Returns:
        bool: bool idicating inclusion

    """
    tag_match = False
    skip_match = False
    if 'tags' in parser:
        if args.tags:
            tag_match = set(args.tags).issubset(set(parser['tags']))
        else:
            tag_match = True
        if args.skip_tags:
            skip_match = any(x in args.skip_tags for x in parser['tags'])
    return tag_match and not skip_match

def load_parsers(devices, args):
    """ Load the parsers for a devices OS, store in device dict

    Args:
        devices (dict): A dict of devices
        args (namespace): The cli args

    Returns:
        dict: A dict of devices, each with parsers attached

    """
    for device in devices:
        if not device['failed']:
            print_log('{:s}: {:s}'.format(device['hostname'], device['os']), 'ljust')
            device['parsers'] = []
            directory = '%s/%s' % (PARSERS, device['os'])
            parser_files = [y for x in os.walk(directory)
                            for y in glob(os.path.join(x[0], '*.yml'))]
            for parser_file in parser_files:
                with open(parser_file, 'r') as stream:
                    try:
                        parsers = yaml.load(stream)
                    except TypeError:
                        device['failed'] = True
                        reason = "Parser appears empty: %s/%s" % (device['os'], parser_file)
                        device['failed_reason'] = reason
                        print_log(reason, 'failed')
                        break
                    except yaml.YAMLError:
                        device['failed'] = True
                        reason = "Error importing parser: %s/%s" % (device['os'], parser_file)
                        device['failed_reason'] = reason
                        print_log(reason, 'failed')
                        break
                for parser in parsers:
                    add_to_device = check_tags(parser, args)
                    if add_to_device:
                        device['parsers'].append(parser)
            else:
                print_log('ok', 'ok')
                continue
    return devices

def load_removers(devices):
    """ Load the removers for a devices OS, store in device dict

    Args:
        devices (dict): A dict of devices

    Returns:
        dict: A dict of devices, each with removers attached

    """
    for device in devices:
        if not device['failed']:
            print_log('{:s}: {:s}'.format(device['hostname'], device['os']), 'ljust')
            device['removers'] = []
            directory = '%s/%s' % (REMOVERS, device['os'])
            remover_files = [y for x in os.walk(directory) \
                             for y in glob(os.path.join(x[0], '*.yml'))]
            for remover_file in remover_files:
                with open(remover_file, 'r') as stream:
                    try:
                        device['removers'].extend(yaml.load(stream))
                    except TypeError:
                        device['failed'] = True
                        reason = "Removers appears empty: %s/%s" % (device['os'], remover_files)
                        device['failed_reason'] = reason
                        print_log(reason, 'failed')
                        break
                    except yaml.YAMLError:
                        device['failed'] = True
                        reason = "Error importing removers: %s/%s" % (device['os'], remover_files)
                        device['failed_reason'] = reason
                        print_log(reason, 'failed')
                        break
            else:
                print_log('ok', 'ok')
                continue
    return devices

def parse(devices):
    """ Run the parsers each device, store in device dict

    Args:
        devices (dict): A dict of devices
        args (dict): A dict of args

    Returns:
        dict: A dict of devices, each with parser results

    """
    for device in devices:
        if not device['failed']:
            device['extractions'] = {}
            for parser in device['parsers']:
                if not device['failed']:
                    parser['used'] = True
                    device = execute_parser(device, parser)
                    if device['failed']:
                        break
            else:
                continue
    return devices

def capture_merge(device, line, current_match, entry):
    """ Run a specific parser entry, store in device dict

    Args:
        device (dict): A device dict
        line (string): The line to parser
        current_match: Any previous capture values
        entry (dict): The specific parser entry to run

    Returns:
        dict: A device, parser result merged into device
        entry: The entry with match values inserted
    """
    matches = re.match(entry['regex'], line)
    num_capture_groups = re.compile(entry['regex']).groups
    if matches and len(matches.groups()) == num_capture_groups:
        if 'captures' in entry:
            for idx, capture in enumerate(entry['captures']):
                if represents_int(matches.groups(0)[idx]):
                    current_match['capture_vars'][capture] = int(matches.groups(0)[idx])
                else:
                    current_match['capture_vars'][capture] = matches.groups(0)[idx]
        full_path = yaml.dump(entry['path'])
        full_path = full_path.replace("\'", "")
        full_path = yaml.load(jinja2.Environment().from_string(full_path) \
                              .render(current_match['capture_vars']))
        device['extractions'] = data_merge(device['extractions'], full_path)
        entry['actual'] = []
        entry['actual'].append(line)
        entry['capture_vars'] = current_match['capture_vars']
        entry['matched'] = True
    else:
        entry['matched'] = False
    return device, entry

def depth(line, current_depth, previous_depth):
    """ Determine the depth of a line (indent)

    Args:
        line (str): The line to analize
        current_depth (dict): A dict for the depth
        previous_depth (dict): A dict of of depth for the previous line

    Returns:
        dict: A dict of devices, each with parsers attached

    """
    smatch = re.match(r'^(\s+)\S.*$', line)
    if smatch:
        current_depth['spaces'] = len(smatch.groups(0)[0])
        if current_depth['spaces'] > previous_depth['spaces']:
            current_depth['depth'] += 1
            current_depth['action'] = 'stepin'
        elif current_depth['spaces'] == previous_depth['spaces']:
            current_depth['action'] = 'stay'
        elif current_depth['spaces'] < previous_depth['spaces']:
            current_depth['action'] = 'stepout'
    else:
        current_depth['depth'] = 0
        current_depth['spaces'] = 0
        current_depth['action'] = 'root'
    return current_depth

def execute_parser(device, parser):
    """ Execute a full parser

    Args:
        device (dict): A device dict

    Returns:
        dict: A dict of devices, each with parsers attached

    """
    print_log('{:s}: {:s}/{:s}'.format(device['hostname'], \
          device['os'], parser['name']), 'ljust')
    capturing = False
    for matcher in parser['matches']:
        logging.info(' MATCHER: %s', matcher['name'])
        matcher['matched'] = False
        matcher['actual'] = []
        matcher['capture_vars'] = {}
        previous_match, next_match = {}, {}
        current_match = matcher
        current_depth = {'depth': 0, 'spaces': 0, 'action': ''}
        capturing = False
        for line in device['configuration']:

            previous_depth = current_depth.copy()
            current_depth = depth(line, current_depth, previous_depth)

            if not capturing and current_depth['action'] != 'root':
                continue

            if 'capture_vars' in current_match and 'delimeter' in current_match['capture_vars']:
                if 'lines' in next_match:
                    current_match = next_match
            else:
                if current_depth['action'] == 'stepin':
                    previous_match = current_match
                    current_match = next_match
                elif current_depth['action'] == 'stepout':
                    current_match = previous_match
                elif current_depth['action'] == 'root':
                    current_match = matcher
                    capturing = False

            if capturing:
                if 'delimeter' in current_match['capture_vars'] and \
                   line.startswith(current_match['capture_vars']['delimeter']):
                    capturing = False
                    matcher['actual'][-1].append(line)
                    current_match = previous_match
                elif 'delimeter' not in current_match['capture_vars'] and \
                    capturing and \
                   (line.startswith('!') or not line.startswith(' ')):
                    capturing = False
                else:
                    if 'lines' in current_match:
                        for entry in current_match['lines']:
                            device, entry = capture_merge(device, line, current_match, entry)
                            if entry['matched']:
                                logging.info('  LINE: %s', line)
                                logging.info('  MATCHED: %s', entry['regex'])
                                matcher['actual'][-1].append(line)
                                next_match = entry
                                capturing = True
            else:
                for entry in current_match['lines']:
                    device, entry = capture_merge(device, line, current_match, entry)
                    if entry['matched']:
                        logging.info('  LINE: %s', line)
                        logging.info('  MATCHED: %s', entry['regex'])
                        matcher['actual'].append([])
                        matcher['actual'][-1].append(line)
                        matcher['matched'] = True
                        next_match = entry
                        capturing = True
        if matcher['matched']:
            device = render_check(device, matcher)
    if not device['failed']:
        print_log('ok', 'ok')
    # else:
    #     print_log(device['failed_reason'], 'failed')
    return device

def run_removers(devices):
    """ Run the removers against devices

    Args:
        devices (dict): A dict of devices

    Returns:
        dict: A dict of devices, post removers

    """
    for device in devices:
        if not device['failed']:
            print_log(device['hostname'], 'ljust')
            device['removals'] = []
            cur_len = len(device['working_configuration'])
            for idx, line in enumerate(reversed(device['working_configuration'])):
                for remover in device['removers']:
                    matches = re.match(remover, line)
                    if matches:
                        device['removals'].insert(0,
                                                  device['working_configuration'].\
                                                  pop(cur_len - idx -1))
            print_log('ok', 'ok')
    return devices

def persist_host_vars(devices, directory, args):
    """ Persist a device vars to fs

    Args:
        devices (dict): A dict of devices
        directory (string): A dir path

    Return:
        dict: The dict of devices updates w/ success/failure
    """
    for device in devices:
        if not device['failed']:
            print_log(device['hostname'], 'ljust')
            host_vars_file = '%s/%s.yml' % (directory, device['hostname'])
            host_vars = {}
            try:
                with open(host_vars_file, 'r') as stream:
                    try:
                        temp_vars = yaml.load(stream)
                        host_vars = temp_vars
                    except TypeError:
                        device['failed'] = True
                        device['failed_reason'] = "Hostvars appears empty."
                        print_log(device['failed_reason'], 'failed')
                    except yaml.YAMLError:
                        device['failed'] = True
                        device['failed_reason'] = "Failed host_vars import."
                        print_log(device['failed_reason'], 'failed')
                clean_vars = remove_keys(device['extractions'], set(['actual']))
                if 'vars' not in host_vars:
                    host_vars['vars'] = {}
                if args.merge_behaviour == 'forward':
                    host_vars['vars'] = data_merge(host_vars['vars'], clean_vars)
                elif args.merge_behaviour == 'reverse':
                    host_vars['vars'] = data_merge(clean_vars, host_vars['vars'])
                elif args.merge_behaviour == 'replace':
                    host_vars['vars'] = clean_vars
                with open(host_vars_file, 'w') as outfile:
                    try:
                        yaml.dump(host_vars, outfile, default_flow_style=False)
                        print_log('ok', 'ok')
                    except yaml.YAMLError:
                        device['failed'] = True
                        device['failed_reason'] = "Failed host_vars export."
            except IOError:
                device['failed'] = True
                reason = "Missing host_vars file for %s" % device['hostname']
                device['failed_reason'] = reason
                print_log(reason, 'failed')
    return devices

def sort_by_ip_as_int(dyct):
    """ Sort a dict keyed by IP as ints

    Args:
        dyct (dict): A dict, with IP addresses as keys

    Return:
        list: A list of tuples, sorted by IP as int
    """
    order_dict = OrderedDict(sorted(dyct.items(),
                                    key=lambda t: \
                                    int(ipaddress.ip_address(unicode(t[0])))))
    return order_dict.items()

def render(tpl_path, context):
    """ Render a jinja template

    Args:
        tpl_path (str): A path to the template
        context (dict): A dict to pass to the teplate

    Return:
        str: an error
    """
    try:
        path, filename = os.path.split(tpl_path)
        env = jinja2.Environment()
        env.trim_blocks=True
        env.filters['sort_by_ip_as_int'] = sort_by_ip_as_int
        env.loader = jinja2.FileSystemLoader(path or './')
        return None, env.get_template(filename).render(context)
    except jinja2.exceptions.TemplateNotFound:
        return 'Template not found. (%s)' % tpl_path, None

def render_check(device, matcher):
    """ Render the template for a parser and check results

    Args:
        device (dict): A device dict
        matcher (dict):

    Returns:
        device (dict): The device dict
    """
    template_name = '{:s}/{:s}/{:s}'.format(TEMPLATES, device['os'], matcher['template'])
    error, raw_results = render(template_name, {'vars': device['extractions']})
    if error:
        device['failed'] = True
        device['failed_reason'] = error
    else:
        try:
            results = (yaml.load(raw_results))
            if not results:
                device['failed'] = True
                device['failed_reason'] = "Jinja template rendered empty. {:s}"\
                                          .format(template_name)
                print_log(device['failed_reason'], 'failed')
                return device
        except yaml.YAMLError:
            device['failed'] = True
            device['failed_reason'] = "Error loading jinja template, invalid yml. {:s}"\
                                      .format(template_name)
            print_log(device['failed_reason'], 'failed')
            print_log(raw_results.split('\n'), )
            return device
        matcher['proposed'] = []
        for result in results:
            matcher['proposed'].append([])
            if result['parents']:
                matcher['proposed'][-1] += result['parents']
            if result['lines']:
                matcher['proposed'][-1] += result['lines']
        matcher['proposed'].sort()
        matcher['actual'].sort()
        diff_pina = [x for x in matcher['proposed'] \
                     if x not in matcher['actual']] + \
                     [x for x in matcher['actual'] if x not in matcher['proposed']]
        if diff_pina:
            device = fail_actual_match(device, matcher, raw_results)
        else:
            matcher['compare_success'] = True
            for match in matcher['proposed']:
                start = (seq_in_seq(match, device['working_configuration']))
                if start != -1:
                    device['working_configuration'] = device['working_configuration'][0:start] +\
                                                      device['working_configuration'][start +\
                                                      len(match):]
                else:
                    device = fail_extract(device, match, raw_results)
    return device

def fail_actual_match(device, matcher, raw_results):
    """ Print debug info for a failed match

    Args:
        device (dict): A device dict
        matcher (dict): The natch
        raw_results (list): The raw results

    Returns:
        dict: The device
    """
    device['failed'] = True
    device['failed_reason'] = "Jinja result does not match actual (%s)." % matcher['name']
    print_log(device['failed_reason'], 'failed')
    print_log('######## EXTRACTIONS')
    print_log(device['extractions'])
    print_log('######## JINJA RESULT RAW')
    print_log(raw_results.split('\n'))
    print_log('######## JINJA RESULT')
    matcher['proposed'].sort()
    print_log(matcher['proposed'])
    print_log('######## ACTUAL')
    print_log(matcher['actual'])
    return device

def fail_extract(device, match, raw_results):
    """ Print debug info for a failed extract

    Args:
        device (dict): A device dict
        match (dict): The natch
        raw_results (list): The raw results

    Returns:
        dict: The device
    """
    device['failed'] = True
    device['failed_reason'] = "Failed to extract jinja output from configuration."
    print_log(device['failed_reason'], 'failed')
    print_log(' ')
    print_log('######## EXTRACTIONS')
    print_log(device['extractions'])
    print_log('######## JINJA RESULT RAW')
    print_log(raw_results.split('\n'))
    print_log('######## JINJA RESULT YAML')
    print_log(match)
    print_log('######## POSSIBLE MATCHES')
    indexes = [i for i, x in enumerate(device['working_configuration'])\
               if x == match[0]]
    for idx in indexes:
        print_log(device['working_configuration'][idx:idx+len(match)+3])
    return device

def report(devices):
    """ Rport the percent complete for each device

    Args:
        devices (dict): A dict of devices
    """
    for device in devices:
        if not device['failed']:
            original = float(len(device['configuration']))
            parsed = float(len(device['working_configuration']))
            percent = (original - parsed)/original
            print_log(device['hostname'], 'ljust')
            if percent == 1:
                print_log("{0:.4f}%".format(percent * 100) +
                          " {:s}/{:s}".format(str(original), str(parsed)), 'ok')
            else:
                print_log("{0:.4f}%".format(percent * 100) +
                          " {:s}/{:s}".format(str(original), str(parsed)), 'warning')

def print_log(message, style=None):
    """ Prints to screen and log file

    Args:
        message (str): The message to print
        style (str): A style with which to print

    """
    header = '\033[95m'
    okgreen = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    endc = '\033[0m'
    logging.debug('FUNCTION: %s', inspect.stack()[1][3])
    if style == 'header':
        print('{:s}*****  {:s} {:s}'.format(header, message, endc))
        logging.info('-------------------------------------------')
        logging.info(message)
        logging.info('-------------------------------------------')
    elif style == 'ljust':
        print(message.ljust(LJUST), end=' ')
        logging.info(message)
    elif style == 'ok':
        print('{:s}[{:s}]      {:s}'.format(okgreen, message, endc))
        logging.info(message)
    elif style == 'warning':
        print('{:s}[{:s}]      {:s}'.format(warning, message, endc))
        logging.info(message)
    elif style == 'failed':
        print('{:s}[fail] {:s}      {:s}'.format(fail, message, endc))
        logging.info(message)
    else:
        pprint(message)
        logging.info(message)

def run(args):
    """ Run all the steps

    Args:
        args (namepsace): The cli args

    """
    print_log('Loading configurations', 'header')
    devices = get_configurations()
    print_log('Copy host_vars entry to temp directory', 'header')
    devices = copy_host_vars(devices, HOST_VARS, HOST_VARS_TEMP)
    print_log('Retrieving OS', 'header')
    devices = get_os(devices)
    print_log('Loading OS removers', 'header')
    devices = load_removers(devices)
    print_log('Loading OS parsers', 'header')
    devices = load_parsers(devices, args)
    print_log('Running parsers and comparing template output to actual', 'header')
    devices = parse(devices)
    print_log('Persist vars to temp directory', 'header')
    devices = persist_host_vars(devices, HOST_VARS_TEMP, args)
    print_log('Copy temp directory to host_vars entry', 'header')
    devices = copy_host_vars(devices, HOST_VARS_TEMP, HOST_VARS)
    print_log('Run removers', 'header')
    devices = run_removers(devices)
    print_log('Report extraction success', 'header')
    report(devices)
    print_log('Remove temp directory', 'header')
    print_log('localhost', 'ljust')
    shutil.rmtree(HOST_VARS_TEMP)
    print_log('ok', 'ok')
    return devices

def main():
    """ Do it all
    """
    parser = ArgumentParser(description='Netork device configuration parser.',
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('--tags', action="store", nargs='+', dest="tags",
                        required=False,
                        help="only run parsers whose tags match these values")
    parser.add_argument('--skip-tags', action="store", nargs='+', dest="skip_tags",
                        required=False,
                        help="only run parsers whose tags do not match these values")
    parser.add_argument('-mb', '--merge_behaviour', action="store", dest="merge_behaviour",
                        required=False, type=str, choices=set(("replace", "forward", "reverse")),
                        default='replace',
                        help="Handle exisiting host_vars entries:\n\
    replace (default): Delete existing vars\n\
    forward: Place new entries on top of previous entries. (WARNING: lists are appended to)\n\
    reverse: Place old entries on top of new entries. (WARNING: lists are appended to)")
    parser.add_argument('-d', '--debug',
                        help="Print debugging information to debug.log",
                        action="store_const", dest="loglevel", const=logging.DEBUG,
                        default=logging.WARNING)
    parser.add_argument('-v', '--verbose',
                        help="Print verbose information to debug.log",
                        action="store_const", dest="loglevel", const=logging.INFO)
    args = parser.parse_args()
    logging.basicConfig(filename='debug.log', level=args.loglevel,
                        format='%(levelname)s: '
                               '%(message)s')
    devices = run(args)
    # for device in devices:
    #     pprint(device['working_configuration'])

if __name__ == "__main__":
    main()
