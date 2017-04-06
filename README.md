# netcopa (Network Configuration Parser)

### Overview

netcopa is an engine which implements a template based state machine for parsing semi-formatted text and storing it as structured data in yaml.

Network device configurations can be converted from text to yaml:

Start with this:
```
!
interface GigabitEthernet1/3
 switchport access vlan 267
 switchport mode access
 switchport voice vlan 867
 spanning-tree portfast
 spanning-tree bpduguard enable
 service-policy input company-user-access-450x
 service-policy output company-user-access-dbl
!
```
Finish with this:

```yaml
interfaces:
  GigabitEthernet1/3:
    name: GigabitEthernet1/3
    service_policies:
    - direction: input
      name: company-user-access-450x
    - direction: output
      name: company-user-access-dbl
    spanning-tree:
      bpduguard: true
      portfast: true
    switchport:
      access:
        vlan: 267
      mode:
      - access
      voice:
        vlan: 867
```

The engine takes four inputs:
  - A network device configuration
  - A hierarchy of parsers
  - A hierarchy of rendering templates, referenced by the parsers
  - An initial variable file for the configuration, indicating the OS of the device

Upon running the engine:
  - Each configuration is loaded into memory
  - The OS is retrieved from the file system (`./host_vars/device_name.yml`)
  - Each parser for the device's OS is added to the device runtime dictionary
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
git clone https://github.com/cidrblock/netcopa
cd netcopa
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

Regular expression always match full lines. This regex captures two pieces of information, the logging type and logging level, stored as `type` and `level` respectively.

The path is treated as a jinja2 template, and the capture values are passed to the jinja2 rendering engine.  The resulting text is:

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

After each extraction, the device's data is passed to the `template` referenced in the parser.  From `./templates/cisco_ios-xe/logging/levels.j2`:


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

The template result is first compared to the lines that were extracted from the configuration. If a match is found the initial full configuration is then walked to find an exact match for the text.  If an exact match is not found, the device will be marked as failed for the remainder of the run.

If a match is found the lines are removed from the configuration and the next parser is run.

### Adding a parser

It will be necessary to add parsers to extract lines not covered by the included parsers.  Please feel free to issue a pull request to have additional parsers added.

The following error is generated when parsing a configuration:

```shell
'######## JINJA RESULT YAML'
['interface GigabitEthernet7/9',
 ' switchport access vlan 267',
 ' switchport mode access',
 ' switchport voice vlan 867',
 ' spanning-tree portfast',
 ' service-policy input company-user-access-450x',
 ' service-policy output company-user-access-dbl']
 '######## POSSIBLE MATCHES'
 ['interface GigabitEthernet7/9',
  ' switchport access vlan 267',
  ' switchport mode access',
  ' switchport voice vlan 867',
  ' spanning-tree portfast',
  ' spanning-tree bpduguard enable',
  ' service-policy input company-user-access-450x',
  ' service-policy output company-user-access-dbl',
  '!',
  'interface GigabitEthernet7/10']
```

The line ` spanning-tree bpduguard enable` is missing from the extraction.  Since this is a cisco_ios-xe device, navigate to `/parsers/cisco_ios-xe/interface` and open the `main.yml` file.

Add the following parser near the bottom above the `service-policy` parser.

```yaml
    - regex: '^ spanning-tree bpduguard enable'
      examples:
      -  ' spanning-tree bpduguard enable'
      path:
        interfaces:
          "{{ name }}":
            spanning-tree:
              bpduguard: True
```

The corresponding temple needs to be modified as well. Open `./templates/cisco_ios-xe/interface/default.j2` and add the following just above `service_policies`:

**Note: Sequence matters.** The jinja template has to produce the exact syntax and sequence of lines found and extracted from the configuration.  This validates the completeness and intergrity of the data.

```jinja
{% if 'spanning-tree' in vars['interfaces'][interface] and 'bpduguard' in vars['interfaces'][interface]['spanning-tree'] and vars['interfaces'][interface]['spanning-tree']['bpduguard'] -%}
- " spanning-tree bpduguard enable"
{% endif -%}{# bpduguard -#}
```

The process would be repeated until the errors are removed.

### Command-line tag and skip-tag support

During the development of parsers or the extraction of data, it may be necessary to focus on subsections of the configuration. Each parser is assigned tags which can be used to either include or exclude the parser from the run.

For instance, to run only the extended ACL parser:
```
python runparse.py --tags ip access-list extended
```

The tags reference the tags found in the parser:

```yaml
- name: ip access-list extended
  tags:
  - ip
  - access-list
  - extended
  matches:
  - name: ip access-list extended
    template: ip/access-lists/extended.j2
    lines:
    - regex: '^ip access-list extended (\S+)$'
      examples:
      - 'ip access-list extended qo-global-core-voice-signal'
      captures:
      - name
      path:
        ip:
          access_lists:
            "{{ name }}":
                name: "{{ name }}"
                type: extended
```

To skip the boot and aaa parsers:

```
python runparse.py --skip-tags extended boot aaa
```
