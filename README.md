# netcopa (Network Configuration Parser)


### Overview

netcopa is an engine which implements a template based state machine for parsing semi-formatted text and storing it as structured data as yaml.

The engine takes four inputs:
  - A network device configuration
  - A hierarchy of parsers
  - A hierarchy of rendering templates, referenced by the parsers
  - An initial variable file for the configuration, indicating the OS

Upon running the engine:
  - Each device configuration is loaded into memory
  - The device's OS is retrieved from the file system
  - Each parser for the device's OS is added to the device record
  - Each parser is run against the configuration, data extracted, rendered with the template and compared back to the initial extraction.  This checks the integrity of the data as well as ensures the data can be used to exactly reproduce the original configuration.
  - Only if the match is successful, the extracted data is written to the filesystem.
  - Extraction success is reported when the engine is complete



### Getting started

Python 2.7+ will need to be installed.
- Clone the repository
- Build a virtual environment
- Install dependancies
- Run the engine against the included sample configurations
- Review the host_vars directory for the resulting yaml extractions

```shell
git clone https://github.com/cidrblock/running-pipe-freedom
cd running-pipe-freedom
virtualenv venv
<...>
source venv/bin/activate
pip install -r requirements.txt
<...>
python runparse.py

*****  Loading configurations
cisco_ios-00                                                           [ok]
cisco_ios-xe-00                                                        [ok]
*****  Copy host_vars entry to temp directory
cisco_ios-00                                                           [ok]
cisco_ios-xe-00                                                        [ok]
*****  Retrieving OS
cisco_ios-00                                                           [ok]
cisco_ios-xe-00                                                        [ok]
*****  Loading OS removers
cisco_ios-00: cisco_ios                                                [ok]
cisco_ios-xe-00: cisco_ios-xe                                          [ok]
*****  Loading OS parsers
cisco_ios-00: cisco_ios                                                [ok]
cisco_ios-xe-00: cisco_ios-xe                                          [ok]
*****  Running parsers and comparing template output to actual
cisco_ios-00: cisco_ios/aaa accounting                                 [ok]
cisco_ios-00: cisco_ios/aaa authentication                             [ok]
cisco_ios-00: cisco_ios/aaa authorization                              [ok]
cisco_ios-00: cisco_ios/aaa groups                                     [ok]
cisco_ios-00: cisco_ios/aaa                                            [ok]
cisco_ios-00: cisco_ios/access-list extended                           [ok]
cisco_ios-00: cisco_ios/access-list standard                           [ok]
cisco_ios-00: cisco_ios/alias                                          [ok]
cisco_ios-00: cisco_ios/banner                                         [ok]
cisco_ios-00: cisco_ios/clock                                          [ok]
cisco_ios-00: cisco_ios/control-plane                                  [ok]
cisco_ios-00: cisco_ios/enable secret                                  [ok]
cisco_ios-00: cisco_ios/hostname                                       [ok]
cisco_ios-00: cisco_ios/interface                                      [ok]
cisco_ios-00: cisco_ios/ip access-list standard                        [ok]
cisco_ios-00: cisco_ios/ip                                             [ok]
cisco_ios-00: cisco_ios/ip prefix-list                                 [ok]
cisco_ios-00: cisco_ios/line con/aux                                   [ok]
cisco_ios-00: cisco_ios/line vty                                       [ok]
cisco_ios-00: cisco_ios/logging                                        [ok]
cisco_ios-00: cisco_ios/ntp servers                                    [ok]
cisco_ios-00: cisco_ios/route-map                                      [ok]
cisco_ios-00: cisco_ios/router eigrp                                   [ok]
cisco_ios-00: cisco_ios/router ospf                                    [ok]
cisco_ios-00: cisco_ios/services                                       [ok]
cisco_ios-00: cisco_ios/snmp-server                                    [ok]
cisco_ios-00: cisco_ios/spanning-tree                                  [ok]
cisco_ios-00: cisco_ios/tacacs-server                                  [ok]
cisco_ios-00: cisco_ios/udld                                           [ok]
cisco_ios-00: cisco_ios/username                                       [ok]
cisco_ios-00: cisco_ios/version                                        [ok]
cisco_ios-00: cisco_ios/vlan                                           [ok]
cisco_ios-xe-00: cisco_ios-xe/aaa accounting                           [ok]
cisco_ios-xe-00: cisco_ios-xe/aaa authentication                       [ok]
cisco_ios-xe-00: cisco_ios-xe/aaa authorization                        [ok]
cisco_ios-xe-00: cisco_ios-xe/aaa groups                               [ok]
cisco_ios-xe-00: cisco_ios-xe/aaa                                      [ok]
cisco_ios-xe-00: cisco_ios-xe/access-list extended                     [ok]
cisco_ios-xe-00: cisco_ios-xe/access-list standard                     [ok]
cisco_ios-xe-00: cisco_ios-xe/alias                                    [ok]
cisco_ios-xe-00: cisco_ios-xe/banner                                   [ok]
cisco_ios-xe-00: cisco_ios-xe/boot                                     [ok]
cisco_ios-xe-00: cisco_ios-xe/class-map                                [ok]
cisco_ios-xe-00: cisco_ios-xe/clock                                    [ok]
cisco_ios-xe-00: cisco_ios-xe/control-plane                            [ok]
cisco_ios-xe-00: cisco_ios-xe/enable secret                            [ok]
cisco_ios-xe-00: cisco_ios-xe/hostname                                 [ok]
cisco_ios-xe-00: cisco_ios-xe/interface                                [ok]
cisco_ios-xe-00: cisco_ios-xe/ip access-list extended                  [ok]
cisco_ios-xe-00: cisco_ios-xe/ip access-list standard                  [ok]
cisco_ios-xe-00: cisco_ios-xe/ip flow                                  [ok]
cisco_ios-xe-00: cisco_ios-xe/ip                                       [ok]
cisco_ios-xe-00: cisco_ios-xe/ip prefix-list                           [ok]
cisco_ios-xe-00: cisco_ios-xe/line con/aux                             [ok]
cisco_ios-xe-00: cisco_ios-xe/line vty                                 [ok]
cisco_ios-xe-00: cisco_ios-xe/logging                                  [ok]
cisco_ios-xe-00: cisco_ios-xe/multilink                                [ok]
cisco_ios-xe-00: cisco_ios-xe/ntp servers                              [ok]
cisco_ios-xe-00: cisco_ios-xe/policy-map                               [ok]
cisco_ios-xe-00: cisco_ios-xe/redundancy                               [ok]
cisco_ios-xe-00: cisco_ios-xe/route-map                                [ok]
cisco_ios-xe-00: cisco_ios-xe/router bgp                               [ok]
cisco_ios-xe-00: cisco_ios-xe/router ospf                              [ok]
cisco_ios-xe-00: cisco_ios-xe/services                                 [ok]
cisco_ios-xe-00: cisco_ios-xe/snmp                                     [ok]
cisco_ios-xe-00: cisco_ios-xe/snmp-server                              [ok]
cisco_ios-xe-00: cisco_ios-xe/spanning-tree                            [ok]
cisco_ios-xe-00: cisco_ios-xe/tacacs-server                            [ok]
cisco_ios-xe-00: cisco_ios-xe/udld                                     [ok]
cisco_ios-xe-00: cisco_ios-xe/username                                 [ok]
cisco_ios-xe-00: cisco_ios-xe/version                                  [ok]
cisco_ios-xe-00: cisco_ios-xe/vlan                                     [ok]
cisco_ios-xe-00: cisco_ios-xe/vrf                                      [ok]
*****  Persist vars to temp directory
cisco_ios-00                                                           [ok]
cisco_ios-xe-00                                                        [ok]
*****  Copy temp directory to host_vars entry
cisco_ios-00                                                           [ok]
cisco_ios-xe-00                                                        [ok]
*****  Run removers
cisco_ios-00                                                           [ok]
cisco_ios-xe-00                                                        [ok]
*****  Report extraction success
cisco_ios-00                                                           [100.0000% 1169.0/0.0]
cisco_ios-xe-00                                                        [100.0000% 2413.0/0.0]
*****  Remove temp directory
localhost                                                              [ok]
```

### Directory layout

The project has a specific directory layout outlined below:

`./configurations`: The directory from which configurations are pulled
`./host_vars`: The directory in which the extracted structured data is stored
`./parsers`: The directory of parsers, organized by OS and global keyword family
`./removers`: Lines that will be removed from the configuration after data extraction, organized by OS
`./templates`: The templates used to recreate the original configuration and validate data integrity, organized by OS and global keywork family
`./utilities`: additional scripts used during development

### Parser and template design

Each parser consists of a regular expression, keywords, and a structured data tree.
- The regular expression is run against the lines of the configuration
- The keywords are used to store the captures from the regular expression
- The tree is then rendered as a template, substituting values for variables.

Formats:

- Parsers are written in yaml, the parser path is treated as a jinja2 template.
- Templates are written in jinja2.
- Extracted data is stored as yaml.

### Simple example:

Using the following configuration subset:

```
!
logging buffered informational
logging console informational
logging monitor informational
!
```
Using a parser located in `./parsers/cisco_ios-xe/logging/main.yml`:

```yaml
- name: logging
  tags:
  - logging
  matches:
  - name: logging levels
    template: logging/levels.j2
    lines:
    - regex: '^logging (buffered|console|monitor) (\w+)$'
      examples:
      - 'logging buffered informational'
      captures:
      - type
      - level
      path:
        logging:
          levels:
          - type: "{{ type }}"
            level: "{{ level }}"
```

Regular expression always match full lines. The regex catures two pieces of information, the logging type and logging level, stored as `type` and `level` respectively.

The path is treated as a jinja template, and the capture values are passed to the jinja2 rendering engine.  The resulting text is:

```yaml
logging:
  levels:
  - level: informational
    type: buffered
  - level: informational
    type: console
  - level: informational
    type: monitor
```

The path is then converted from yaml to a python dictionary and stored as extracted data for the device.

After each extraction, the device's data is passwed to the `template` refernced in the parser.  From `./templates/cisco_ios-xe/logging/levels.j2`:


```jinja
{% for entry in vars['logging']['levels'] -%}
- parents:
  lines:
  - 'logging {{ entry['type'] }} {{ entry['level'] }}'
{% endfor -%}
```

The template produces yaml.  Both parents and lines can be generated.  Parents and lines are convenience keys to aid in the use of the template for later automation.

The template result would be as follows:

```yaml
- parents:
  lines:
  - logging buffered informational
  - logging console informational
  - logging monitor informational
```

The engine combines the parents and lines into a single list of values:

```text
logging buffered informational
logging console informational
logging monitor informational
```

The jinja result is first compared to the lines that were extracted. If a match is found the initial full configuration is then walked to find an exact match for the text.  If an exact match is not found, the device will be marked as failed for the remainder of the run.

If a match is found the lines are removed from the configration and the next parser is run.
