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

def load_host_vars(device):
    """ Load the host_vars file for a device

    Args:
        device (dict): A dict of a device

    Returns:
        dict: The devices with it's host_varss added
    """
    try:
        with open('%s/%s.yml' % (HOST_VARS, device['hostname']), 'r') as stream:
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
        env.filters['sort_by_ip_as_int'] = sort_by_ip_as_int
        env.loader = jinja2.FileSystemLoader(path or './')
        return None, env.get_template(filename).render(context)
    except jinja2.exceptions.TemplateNotFound:
        return 'Template not found. (%s)' % tpl_path, None

def render_add_to_final(device, template_name):
    """ Render the template for a parser and check results

    Args:
        device (dict): A device dict
        template_name (str): The name of a template

    Returns:
        device (dict): The device dict
    """
    if not 'reborn' in device:
        device['reborn'] = []
    print_log('{:s} {:s}'.format(device['hostname'], ('/').join(template_name.split('/')[2:])), 'ljust')
    error, raw_results = render(template_name, {'vars': device['vars']})
    if error:
        device['failed'] = True
        device['failed_reason'] = error
    else:
        try:
            results = (yaml.load(raw_results))
            used = False
            if results:

                for result in results:
                    if result['parents'] or result['lines']:
                        used = True
                    if result['parents']:
                        device['reborn'] += '!'
                        device['reborn'].extend(result['parents'])
                    if result['lines']:
                        device['reborn'].extend(result['lines'])
            if used:
                print_log('ok', 'ok')
            else:
                print_log('skipped', 'warning')
        except yaml.YAMLError:
            device['failed'] = True
            device['failed_reason'] = "Error loading jinja template, invalid yml. {:s}"\
                                      .format(template_name)
            print_log(device['failed_reason'], 'failed')
            print_log(raw_results.split('\n'), )
            return device
    return device

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

def iterate_templates(devices):
    for device in devices:
        directory = '%s/%s' % (TEMPLATES, device['os'])
        template_files = [y for x in os.walk(directory)
                          for y in glob(os.path.join(x[0], '*.j2'))]
        for template_file in template_files:
            render_add_to_final(device, template_file)
    return devices

def save_config(devices):
    newdir = CONFIGURATIONS_DIR + '_rebuilt'
    if not os.path.exists(newdir):
        os.makedirs(newdir)
    for device in devices:
        print_log(device['hostname'], 'ljust')
        ofile = open('{:s}/{:s}.cfg'.format(newdir, device['hostname']), 'w')
        ofile.write("\n".join(device['reborn']))
        print_log( 'ok', 'ok')

def run(args):
    """ Run all the steps

    Args:
        args (namepsace): The cli args

    """
    print_log('Loading configurations', 'header')
    devices = get_configurations()
    print_log('Retrieving OS', 'header')
    devices = get_os(devices)
    print_log('Rebuilding config', 'header')
    devices = iterate_templates(devices)
    print_log('Writing rebuilt config to file', 'header')
    save_config(devices)
    return devices

def main():
    """ Do it all
    """
    parser = ArgumentParser(description='Netork device configuration parser.',
                            formatter_class=RawTextHelpFormatter)
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
    #     pprint(device['reborn'])

if __name__ == "__main__":
    main()
