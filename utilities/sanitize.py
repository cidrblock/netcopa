import re
from argparse import ArgumentParser
import faker
from pprint import pprint
import yaml


fake = faker.Factory.create()
last_match = ''
last_fake = ''
last_fourth = 0

def swap_ip(line):
    global last_match
    global last_fourth
    global last_fake
    if line.startswith('!'):
        last_fourth = 0
    regex = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    for match in re.findall(regex, line):
        if match.startswith('0.'):
            # print 'Found "%s" is a reverse mask, leaving' % match
            pass
        elif match.startswith('255.'):
            # print 'Found "%s" is a mask, leaving' % match
            pass
        elif match.startswith('10.'):
            if match == last_match:
                new = last_fake
            elif last_fourth > int(match.split('.')[3]):
                new = '10.0.0.' + str(last_fourth + 1)
                last_fourth = int(last_fourth) + 1
                last_match = match
                last_fake = new
            else:
                new = '10.0.0.' + match.split('.')[3]
                last_fourth = int(match.split('.')[3])
                last_match = match
                last_fake = new
            line = line.replace(match, new)
        else:
            if match == last_match:
                new = last_fake
                last_match = match
            else:
                new = fake.ipv4(network=False)
                last_match = match
                last_fake = new
            line = line.replace(match, new)
    return line

def swap_pass(line):
    regex = r'((password|secret|key) \d .*)'
    for match in re.findall(regex, line):
        line = line.replace(match[0].split()[2], 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return line

def swap_community(line):
    regex = r'(community (\S+))'
    for match in re.findall(regex, line):
        line = line.replace(match[1], 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return line

def swap_location(line):
    regex = r'(snmp-server location (.*))'
    for match in re.findall(regex, line):
        line = line.replace(match[1], fake.address().replace('\n',', '))
    return line

def swap_contact(line):
    regex = r'(snmp-server contact (.*))'
    for match in re.findall(regex, line):
        line = line.replace(match[1], fake.email())
    return line

def swap_desc(line):
    regex = r'(description (.*))'
    for match in re.findall(regex, line):
        replace = match[1]
        length = len(replace)
        if len(replace) < 6:
            length = 5
        line = line.replace(replace, fake.text(length))
    return line

def swap_remark(line):
    regex = r'(remark (.*))'
    for match in re.findall(regex, line):
        replace = match[1]
        length = len(replace)
        if len(replace) < 6:
            length = 5
        line = line.replace(replace, fake.text(length))

    return line

def swap_keywords(line,keywords):
    for keyword in keywords:
        regex = keyword['word']
        for match in re.findall(regex, line):
            line = line.replace(match, keyword['replace'])
    return line

def main():
    """ Do it all
    """
    parser = ArgumentParser(description='Does some basic config cleaning.')
    parser.add_argument('--file', action="store", type=str, dest="filename",
                        required=True,
                        help="The file to clean.")

    args = parser.parse_args()
    new_config = []

    with open(args.filename) as f:
        content = f.readlines()
    with open('keywords.yml') as stream:
        keywords = yaml.load(stream)
    for line in content:
        line = swap_ip(line)
        line = swap_pass(line)
        line = swap_community(line)
        line = swap_location(line)
        line = swap_contact(line)
        line = swap_desc(line)
        line = swap_remark(line)
        line = swap_keywords(line, keywords)

        new_config.append(line)

    thefile = open('test.cfg', 'w')

    for line in new_config:
        thefile.write(line)

    # pprint(new_config)


if __name__ == "__main__":
    main()
