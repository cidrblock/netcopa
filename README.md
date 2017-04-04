```
➜  running-pipe-freedom git:(readme) ✗ virtualenv venv
New python executable in /Users/me/github/running-pipe-freedom/venv/bin/python
Installing setuptools, pip, wheel...done.
➜  running-pipe-freedom git:(readme) ✗ source venv/bin/activate
(venv) ➜  running-pipe-freedom git:(readme) ✗ pip install -r requirements.txt
<...>
(venv) ➜  running-pipe-freedom git:(readme) ✗ python runparse.py
***** Loading configurations
chddc1crt001.starbucks.net                                             [ok]
seassclrt001.starbucks.net                                             [ok]
***** Copy host_vars entry to temp directory
chddc1crt001.starbucks.net                                             [ok]
seassclrt001.starbucks.net                                             [ok]
***** Retrieving OS
chddc1crt001.starbucks.net                                             [ok]
seassclrt001.starbucks.net                                             [ok]
***** Loading OS removers
chddc1crt001.starbucks.net: cisco_ios-xe                               [ok]
seassclrt001.starbucks.net: cisco_ios                                  [ok]
***** Loading OS parsers
chddc1crt001.starbucks.net: cisco_ios-xe                               [ok]
seassclrt001.starbucks.net: cisco_ios                                  [ok]
***** Running parsers and comparing template output to actual
chddc1crt001.starbucks.net: cisco_ios-xe/aaa accounting                [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/aaa authentication            [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/aaa authorization             [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/aaa groups                    [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/aaa                           [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/access-list extended          [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/access-list standard          [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/alias                         [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/banner                        [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/boot                          [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/class-map                     [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/clock                         [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/control-plane                 [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/enable secret                 [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/hostname                      [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/interface                     [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/ip access-list extended       [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/ip access-list standard       [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/ip flow                       [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/ip                            [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/ip prefix-list                [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/line con/aux                  [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/line vty                      [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/logging                       [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/multilink                     [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/ntp servers                   [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/policy-map                    [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/redundancy                    [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/route-map                     [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/router bgp                    [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/router eigrp                  [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/router ospf                   [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/services                      [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/snmp                          [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/snmp-server                   [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/spanning-tree                 [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/tacacs-server                 [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/udld                          [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/username                      [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/version                       [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/vlan                          [ok]
chddc1crt001.starbucks.net: cisco_ios-xe/vrf                           [ok]
seassclrt001.starbucks.net: cisco_ios/aaa accounting                   [ok]
seassclrt001.starbucks.net: cisco_ios/aaa authentication               [ok]
seassclrt001.starbucks.net: cisco_ios/aaa authorization                [ok]
seassclrt001.starbucks.net: cisco_ios/aaa groups                       [ok]
seassclrt001.starbucks.net: cisco_ios/aaa                              [ok]
seassclrt001.starbucks.net: cisco_ios/access-list extended             [ok]
seassclrt001.starbucks.net: cisco_ios/access-list standard             [ok]
seassclrt001.starbucks.net: cisco_ios/alias                            [ok]
seassclrt001.starbucks.net: cisco_ios/banner                           [ok]
seassclrt001.starbucks.net: cisco_ios/clock                            [ok]
seassclrt001.starbucks.net: cisco_ios/control-plane                    [ok]
seassclrt001.starbucks.net: cisco_ios/enable secret                    [ok]
seassclrt001.starbucks.net: cisco_ios/hostname                         [ok]
seassclrt001.starbucks.net: cisco_ios/interface                        [ok]
seassclrt001.starbucks.net: cisco_ios/ip access-list standard          [ok]
seassclrt001.starbucks.net: cisco_ios/ip                               [ok]
seassclrt001.starbucks.net: cisco_ios/ip prefix-list                   [ok]
seassclrt001.starbucks.net: cisco_ios/line con/aux                     [ok]
seassclrt001.starbucks.net: cisco_ios/line vty                         [ok]
seassclrt001.starbucks.net: cisco_ios/logging                          [ok]
seassclrt001.starbucks.net: cisco_ios/ntp servers                      [ok]
seassclrt001.starbucks.net: cisco_ios/route-map                        [ok]
seassclrt001.starbucks.net: cisco_ios/router eigrp                     [ok]
seassclrt001.starbucks.net: cisco_ios/router ospf                      [ok]
seassclrt001.starbucks.net: cisco_ios/services                         [ok]
seassclrt001.starbucks.net: cisco_ios/snmp                             [ok]
seassclrt001.starbucks.net: cisco_ios/snmp-server                      [ok]
seassclrt001.starbucks.net: cisco_ios/spanning-tree                    [ok]
seassclrt001.starbucks.net: cisco_ios/tacacs-server                    [ok]
seassclrt001.starbucks.net: cisco_ios/udld                             [ok]
seassclrt001.starbucks.net: cisco_ios/username                         [ok]
seassclrt001.starbucks.net: cisco_ios/version                          [ok]
seassclrt001.starbucks.net: cisco_ios/vlan                             [ok]
***** Persist vars to temp directory
chddc1crt001.starbucks.net                                             [ok]
seassclrt001.starbucks.net                                             [ok]
***** Copy temp directory to host_vars entry
chddc1crt001.starbucks.net                                             [ok]
seassclrt001.starbucks.net                                             [ok]
***** Run removers
chddc1crt001.starbucks.net                                             [ok]
seassclrt001.starbucks.net                                             [ok]
***** Report extraction success
chddc1crt001.starbucks.net                                             100.0000% (2413.0/0.0)
seassclrt001.starbucks.net                                             100.0000% (1169.0/0.0)
***** Remove temp directory
localhost                                                              [ok]
Press Enter to for remaining config or control-c...
```
