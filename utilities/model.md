### aaa accounting exec
```yaml
aaa:
  accounting:
    connection:
      default:
        events: '{{ events }}'
        methods: '{{ groups.replace("group", "^group").split("^")[1:] + methods.split(''
          '') }}'
    exec:
      default:
        events: '{{ events }}'
        methods: '{{ groups.replace("group", "^group").split("^")[1:] + methods.split(''
          '') }}'
    system:
      default:
        events: '{{ events }}'
        methods: '{{ groups.replace("group", "^group").split("^")[1:] + methods.split(''
          '') }}'

```
### aaa authentication login
```yaml
aaa:
  authentication:
    login:
      activated:
        methods:
        - '{{ methods.split('' '') }}'
      default:
        methods: '{{ groups.replace("group", "^group").split("^")[1:] + methods.split(''
          '') }}'

```
### aaa authorization
```yaml
aaa:
  authorization:
    commands:
      default:
        methods: '{{ groups.replace("group", "^group").split("^")[1:] + methods.split(''
          '') }}'
        privilege_level: '{{ privilege_level }}'
    '{{ aaa_kind }}':
      activated:
        methods: '{{ groups.replace("group ", "^group ").split("^")[1:] + methods.split(''
          '') }}'
      default:
        methods: '{{ groups.replace("group", "^group").split("^")[1:] + methods.split(''
          '') }}'

```
### aaa group
```yaml
aaa:
  groups:
    '{{ group_name }}':
      name: '{{ group_name }}'
      servers:
      - encryption_type: '{{ encryption_type }}'
        ip: '{{ server_private_ip }}'
        key: '{{ key }}'
        private: true
      tacacs_source_interface: '{{ source_interface }}'
      type: '{{ group_type }}'

```
### aaa session-id
```yaml
aaa:
  new_model: true
  session_id: '{{ session_id }}'

```
### access-list extended
```yaml
access_lists:
  '{{ number }}':
    entries:
    - action: '{{ action }}'
      destination_network: '{{ destination_network }}'
      destination_wildcard: 0.0.0.0
      protocol: '{{ protocol }}'
      source_network: any
      source_wildcard: any
      whitespace: '"{{ whitespace }}"'
    number: '{{ number  }}'
    type: extended

```
### access-list standard
```yaml
access_lists:
  '{{ number }}':
    entries:
    - action: '{{ action }}'
      source_network: '{{ source_network }}'
      source_wildcard: 0.0.0.0
      whitespace: '"{{ whitespace }}"'
    - action: '{{ action }}'
      source_network: '{{ source_network }}'
      source_wildcard: any
      whitespace: '"{{ whitespace }}"'
    - action: '{{ action }}'
      source_network: '{{ source_network }}'
      source_wildcard: '{{ source_wildcard }}'
      whitespace: '"{{ whitespace }}"'
    - remark: '{{ remark }}'
    number: '{{ number  }}'
    type: standard

```
### alias
```yaml
aliases:
- alias: '{{ alias }}'
  command: '{{ command }}'
  mode: '{{ mode }}'

```
### banner
```yaml
banner:
  '{{ type }}':
    delimeter: '{{ delimeter }}'
    text:
    - '"{{ text_line }}"'

```
### boot
```yaml
boot:
  system:
  - filename: '{{ filename }}'
    flash_fs: '{{ flash_fs }}'
    from: flash

```
### class-map
```yaml
class_maps:
  '{{ name }}':
    entries:
    - dscp_values: '{{ dscp_values.split() }}'
      type: dscp
    - name: '{{ access_group_name }}'
      type: access-group
    match_type: '{{ match_type }}'
    name: '{{ name }}'

```
### clock timezone
```yaml
clock:
  hours_offset: '{{ hours_offset }}'
  minutes_offset: '{{ minutes_offset }}'
  timezone: '{{ timezone }}'

```
### control-plane
```yaml
control_plane: null

```
### enable secret
```yaml
enable:
  secret:
    encryption_type: '{{ encryption_type }}'
    secret: '{{ secret }}'

```
### hostname
```yaml
hostname: '{{ hostname }}'

```
### interface
```yaml
interfaces:
  '{{ name }}':
    bandwidth: '{{ bandwidth }}'
    channel_group: '{{ channel_group }}'
    channel_group_mode: '{{ channel_group_mode.split() }}'
    description: '"{{ description }}"'
    encapsulation:
      protocol: '{{ encapsulation_protocol }}'
      tag: '{{ encapsulation_tag }}'
    ip:
      address:
        ipv4_address: '{{ ipv4_address }}'
        ipv4_netmask: '{{ ipv4_netmask }}'
        negate: true
      flow:
        directions:
        - '{{ flow_direction }}'
      pim:
        mode: '{{ pim_mode }}'
    name: '{{ name }}'
    negotiation:
      negate: true
      type: '{{ negotiation }}'
    service_policies:
    - direction: '{{ service_policy_direction }}'
      name: '{{ service_policy_name }}'
    shutdown: true
    spanning-tree:
      bpduguard: true
      portfast: true
    switchport:
      access:
        vlan: '{{ vlan }}'
      mode: '{{ mode.split() }}'
      negate: true
      present: true
      trunk:
        allowed_vlans:
          add: '"{{ vlans }}"'
          vlans: '"{{ vlans }}"'
        native_vlan: '{{ vlan }}'
      voice:
        vlan: '{{ voice_vlan }}'
    vrf: '{{ vrf }}'

```
### ip access-list extended
```yaml
ip:
  access_lists:
    '{{ name }}':
      entries:
      - action: '{{ action }}'
        destination_network: 0.0.0.0
        destination_wildcard: 255.255.255.255
        protocol: '{{ protocol }}'
        source_network: 0.0.0.0
        source_wildcard: 255.255.255.255
      - action: '{{ action }}'
        destination_network: '{{ destination_network }}'
        destination_wildcard: 0.0.0.0
        protocol: '{{ protocol }}'
        source_network: 0.0.0.0
        source_wildcard: 255.255.255.255
      - action: '{{ action }}'
        destination_network: 0.0.0.0
        destination_wildcard: 255.255.255.255
        protocol: '{{ protocol }}'
        source_network: '{{ source_network }}'
        source_wildcard: 0.0.0.0
      - action: '{{ action }}'
        destination_network: '{{ destination_network }}'
        destination_wildcard: 0.0.0.0
        protocol: '{{ protocol }}'
        source_network: '{{ source_network }}'
        source_wildcard: '{{ source_wildcard }}'
      - action: '{{ action }}'
        destination_network: '{{ destination_network }}'
        destination_wildcard: '{{ destination_wildcard }}'
        protocol: '{{ protocol }}'
        source_network: '{{ source_network }}'
        source_wildcard: 0.0.0.0
      - action: '{{ action }}'
        destination_network: 0.0.0.0
        destination_port: '{{ destination_port }}'
        destination_wildcard: 255.255.255.255
        protocol: '{{ protocol }}'
        source_network: 0.0.0.0
        source_wildcard: 255.255.255.255
      - action: '{{ action }}'
        destination_network: 0.0.0.0
        destination_wildcard: 255.255.255.255
        protocol: '{{ protocol }}'
        source_network: 0.0.0.0
        source_port: '{{ source_port }}'
        source_wildcard: 255.255.255.255
      - action: '{{ action }}'
        destination_network: 0.0.0.0
        destination_wildcard: 255.255.255.255
        protocol: '{{ protocol }}'
        source_network: '{{ source_network }}'
        source_port: '{{ source_port }}'
        source_wildcard: 0.0.0.0
      - action: '{{ action }}'
        destination_network: 0.0.0.0
        destination_port: '{{ destination_port }}'
        destination_wildcard: 255.255.255.255
        protocol: '{{ protocol }}'
        source_network: '{{ source_network }}'
        source_wildcard: 0.0.0.0
      - action: '{{ action }}'
        destination_network: '{{ destination_network }}'
        destination_port: '{{ destination_port }}'
        destination_wildcard: 0.0.0.0
        protocol: '{{ protocol }}'
        source_network: 0.0.0.0
        source_wildcard: 255.255.255.255
      - action: '{{ action }}'
        destination_network: '{{ destination_network }}'
        destination_port: '{{ destination_port }}'
        destination_wildcard: '{{ destination_wildcard }}'
        protocol: '{{ protocol }}'
        source_network: 0.0.0.0
        source_wildcard: 255.255.255.255
      - action: '{{ action }}'
        destination_network: 0.0.0.0
        destination_wildcard: 255.255.255.255
        protocol: '{{ protocol }}'
        source_network: '{{ source_network }}'
        source_port: '{{ source_port }}'
        source_wildcard: '{{ source_wildcard }}'
      - action: '{{ action }}'
        destination_network: 0.0.0.0
        destination_port: '{{ destination_port }}'
        destination_wildcard: 255.255.255.255
        protocol: '{{ protocol }}'
        source_network: '{{ source_network }}'
        source_wildcard: '{{ source_wildcard }}'
      - action: '{{ action }}'
        destination_network: '{{ destination_network }}'
        destination_port: '{{ destination_port }}'
        destination_wildcard: 0.0.0.0
        protocol: '{{ protocol }}'
        source_network: '{{ source_network }}'
        source_wildcard: '{{ source_wildcard }}'
      - action: '{{ action }}'
        destination_network: '{{ destination_network }}'
        destination_wildcard: '{{ destination_wildcard }}'
        protocol: '{{ protocol }}'
        source_network: '{{ source_network }}'
        source_port: '{{ source_port }}'
        source_wildcard: 0.0.0.0
      - action: '{{ action }}'
        destination_network: '{{ destination_network }}'
        destination_port: '{{ destination_port }}'
        destination_wildcard: '{{ destination_wildcard }}'
        protocol: '{{ protocol }}'
        source_network: '{{ source_network }}'
        source_wildcard: '{{ source_wildcard }}'
      - action: '{{ action }}'
        destination_network: '{{ destination_network }}'
        destination_wildcard: '{{ destination_wildcard }}'
        protocol: '{{ protocol }}'
        source_network: '{{ source_network }}'
        source_port: '{{ source_port }}'
        source_wildcard: '{{ source_wildcard }}'
      - action: '{{ action }}'
        destination_end_port: '{{ destination_end_port }}'
        destination_network: 0.0.0.0
        destination_start_port: '{{ destination_start_port }}'
        destination_wildcard: 255.255.255.255
        protocol: '{{ protocol }}'
        source_network: 0.0.0.0
        source_wildcard: 255.255.255.255
      - action: '{{ action }}'
        destination_network: 0.0.0.0
        destination_wildcard: 255.255.255.255
        protocol: '{{ protocol }}'
        source_end_port: '{{ source_end_port }}'
        source_network: 0.0.0.0
        source_start_port: '{{ source_start_port }}'
        source_wildcard: 255.255.255.255
      - action: '{{ action }}'
        destination_network: 0.0.0.0
        destination_wildcard: 255.255.255.255
        protocol: '{{ protocol }}'
        source_end_port: '{{ source_end_port }}'
        source_network: '{{ source_network }}'
        source_start_port: '{{  source_start_port }}'
        source_wildcard: '{{ source_wildcard }}'
      - action: '{{ action }}'
        destination_network: 0.0.0.0
        destination_wildcard: 255.255.255.255
        protocol: '{{ protocol }}'
        source_end_port: '{{ source_end_port }}'
        source_network: '{{ source_network }}'
        source_start_port: '{{ source_start_port }}'
        source_wildcard: 0.0.0.0
      - action: '{{ action }}'
        destination_end_port: '{{ destination_end_port }}'
        destination_network: 0.0.0.0
        destination_start_port: '{{ destination_start_port }}'
        destination_wildcard: 255.255.255.255
        protocol: '{{ protocol }}'
        source_network: '{{ source_network }}'
        source_wildcard: 0.0.0.0
      - action: '{{ action }}'
        destination_end_port: '{{ destination_end_port }}'
        destination_network: '{{ destination_network }}'
        destination_start_port: '{{ destination_start_port }}'
        destination_wildcard: 0.0.0.0
        protocol: '{{ protocol }}'
        source_network: 0.0.0.0
        source_wildcard: 255.255.255.255
      - action: '{{ action }}'
        destination_end_port: '{{ destination_end_port }}'
        destination_network: 0.0.0.0
        destination_start_port: '{{ destination_start_port }}'
        destination_wildcard: 255.255.255.255
        protocol: '{{ protocol }}'
        source_network: '{{ source_network }}'
        source_wildcard: '{{ source_wildcard}}'
      - action: '{{ action }}'
        destination_network: '{{ destination_network }}'
        destination_wildcard: '{{ destination_wildcard }}'
        protocol: '{{ protocol }}'
        source_end_port: '{{ source_end_port }}'
        source_network: 0.0.0.0
        source_start_port: '{{ source_start_port }}'
        source_wildcard: 255.255.255.255
      - action: '{{ action }}'
        destination_end_port: '{{ destination_end_port }}'
        destination_network: '{{ destination_network }}'
        destination_start_port: '{{ destination_start_port }}'
        destination_wildcard: '{{ destination_wildcard }}'
        protocol: '{{ protocol }}'
        source_network: 0.0.0.0
        source_wildcard: 255.255.255.255
      - action: '{{ action }}'
        destination_network: '{{ destination_network }}'
        destination_wildcard: '{{ destination_wildcard }}'
        protocol: '{{ protocol }}'
        source_end_port: '{{ source_end_port }}'
        source_network: '{{ source_network }}'
        source_start_port: '{{ source_start_port }}'
        source_wildcard: '{{ source_wildcard }}'
      - action: '{{ action }}'
        destination_end_port: '{{ destination_end_port }}'
        destination_network: '{{ destination_network }}'
        destination_start_port: '{{ destination_start_port }}'
        destination_wildcard: '{{ destination_wildcard }}'
        protocol: '{{ protocol }}'
        source_network: '{{ source_network }}'
        source_wildcard: '{{ source_wildcard }}'
      - action: '{{ action }}'
        destination_dscp: '{{ destination_dscp }}'
        destination_network: 0.0.0.0
        destination_wildcard: 255.255.255.255
        protocol: '{{ protocol }}'
        source_network: 0.0.0.0
        source_wildcard: 255.255.255.255
      - remark: '"{{ remark }}"'
      - remark: null
      name: '{{ name }}'
      type: extended

```
### ip access-list standard
```yaml
ip:
  access_lists:
    '{{ name }}':
      entries:
      - action: '{{ action }}'
        source_network: '{{ source_network }}'
        source_wildcard: 0.0.0.0
      - action: '{{ action }}'
        source_network: '{{ source_network }}'
        source_wildcard: any
      - action: '{{ action }}'
        source_network: '{{ source_network }}'
        source_wildcard: '{{ source_wildcard }}'
      - remark: '"{{ remark }}"'
      - remark: null
      name: '{{ name }}'
      type: standard

```
### ip flow-export
```yaml
ip:
  flow_cache:
    timeout:
      active:
        minutes: '{{ active_timeout }}'
  flow_export:
    destinations:
    - ipv4_address: '{{ destination }}'
      port: '{{ destination_port }}'
    source: '{{ source }}'
    version: '{{ source }}'

```
### ip multicast routing distributed
```yaml
ip:
  classless: true
  domain_lists:
  - domain_name: '{{ domain_list }}'
  domain_names:
  - domain_name: '{{ domain_name }}'
  http:
    secure_server: false
    server: false
  multicast_routing:
    distributed: true
    enabled: true
  name-servers:
  - name_server: '{{ name_server_ip }}'
  ospf_name-lookup: true
  pim:
    rp_address: '{{ rp_address }}'
  routes:
  - netmask: '{{ netmask }}'
    network: '{{ network }}'
    next_hop: '{{ next_hop }}'
  source-route: true
  subnet-zero: true
  tacacs:
    source_interface: '{{ source_interface }}'

```
### ip prefix-list
```yaml
ip:
  prefix_lists:
    '{{ name }}':
      entries:
      - action: '{{ action }}'
        netmask: '{{ netmask }}'
        network: '{{ network }}'
        sequence: '{{ sequence }}'
      - action: '{{ action }}'
        le_bits: '{{ le_bits }}'
        netmask: '{{ netmask }}'
        network: '{{ network }}'
        sequence: '{{ sequence }}'
      name: '{{ name }}'

```
### line con
```yaml
line:
  '{{ type }}':
    numbers:
      '{{ number }}':
        escape_character: '{{ escape_character }}'
        exec_timeout:
          minutes: '{{ minutes }}'
          seconds: '{{ seconds }}'
        login:
          authentication: '{{ named_list }}'
        number: '{{ number }}'
        password:
          encryption_type: '{{ encryption_type }}'
          password: '{{ password }}'
        stopbits: '{{ stopbits }}'
        transport:
          '{{ direction }}':
            protocols: '{{ protocols.split() }}'
    type: '{{ type }}'

```
### line con
```yaml
line:
  vty:
    '{{ start }}to{{ finish }}':
      escape_character: '{{ escape_character }}'
      exec_timeout:
        minutes: '{{ minutes }}'
        seconds: '{{ seconds }}'
      finish: '{{ finish }}'
      password:
        encryption_type: '{{ encryption_type }}'
        password: '{{ password }}'
      privilege_level: '{{ privilege_level }}'
      start: '{{ start }}'
      transport:
        '{{ direction }}':
          protocols: '{{ protocols.split() }}'

```
### logging source
```yaml
logging:
  facility: '{{ facility }}'
  hosts:
  - host: '{{ host }}'
  levels:
  - level: '{{ level }}'
    type: '{{ type }}'
  source_interface: '{{ source_interface }}'

```
### multilink
```yaml
multilink:
  bundle_name:
    method: '{{ method }}'

```
### ntp source
```yaml
ntp:
  servers:
  - server_ip: '{{ server_ip }}'
  source:
    interface: '{{ interface }}'

```
### policy-map
```yaml
policy_maps:
  '{{ policy_name }}':
    classes:
      '{{ class_name }}':
        name: '{{ class_name }}'
    description: '"{{ description }}"'
    name: '{{ policy_name }}'
    sequence:
    - '{{ class_name }}'

```
### redundancy
```yaml
redundancy:
  enabled: true
  mode: '{{ mode }}'

```
### route-map
```yaml
route_maps:
  '{{ name }}':
    name: '{{ name }}'
    statements:
      '{{ sequence }}':
        action: '{{ action }}'
        clauses:
        - clause: '{{ clause }}'
          value: '"{{ value }}"'
        sequence: '{{ sequence }}'

```
### router bgp
```yaml
router:
  bgp:
    '{{ parent_process_id }}':
      address_families:
        '"{{ ip_version }}"':
          ip_version: '{{ ip_version }}'
          vrfs:
            '{{ vrf_name }}':
              vrf_name: '{{ vrf_name }}'
      address_family_delimeter: bang
      address_family_exit_command: exit-address-family
      aggregate_addresses:
      - netmask: '{{ aggregate_netmask }}'
        network: '{{ aggregate_address }}'
        summary_only: true
      auto_summary: false
      log_neighbor_changes: true
      neighbors:
        '{{ ipv4_address }}':
          default_originate:
            enabled: true
            route_map: '{{ default_originate_route_map }}'
          description: '"{{ description }}"'
          ipv4_address: '{{ ipv4_address }}'
          next_hop_self: true
          remote_as: '{{ remote_as }}'
          route_map_in: '{{ route_map_in }}'
          route_map_out: '{{ route_map_out }}'
          soft_reconfiguration_inbound: true
      process_id: '{{ parent_process_id }}'
      redistribute:
        ospf:
          match:
          - internal
          - external 1
          - external 2
          process_id: '{{ process_id}}'
          protocol: ospf
          route_map: '{{ route_map }}'
        '{{ protocol }}':
          protocol: '{{ protocol }}'
      router_id: '{{ router_id }}'
      synchronization: false

```
### router ospf
```yaml
router:
  ospf:
    '{{ parent_process_id }}':
      auto_cost_reference_bandwidth: '{{ reference_bandwidth }}'
      default_information:
        metric: '{{ metric }}'
        metric_type: '{{ metric_type }}'
        originate: true
      distance: '{{ distance }}'
      distribute_lists:
      - &id001
        direction: '{{ direction }}'
        route_map: '{{ distribute_list_route_map }}'
      - *id001
      log_adjacency_changes: true
      network_statements:
      - &id002
        area: '{{ network_area }}'
        netmask: '{{ network_netmask }}'
        network: '{{ network_network }}'
      - *id002
      passive_interface_default: true
      passive_interfaces:
      - &id003
        interface: '{{ no_passive_interface }}'
        negate: true
      - *id003
      process_id: '{{ parent_process_id }}'
      redistribute:
        static:
          protocol: static
          subnets: true
        '{{ protocol }}':
          metric: '{{ metric }}'
          metric_types: '{{ metric_types.replace("metric-type", "").split('' '') }}'
          process_id: '{{ redist_process_id }}'
          protocol: '{{ protocol }}'
          route_map: '{{ route_map }}'
          subnets: true
          tag: '{{ tag }}'
      router_id: '{{ router_id }}'
      summary_addresses:
      - &id004
        netmask: '{{ summary_netmask }}'
        network: '{{ summary_network }}'
      - *id004
      vrf: '{{ vrf }}'

```
### disabled services
```yaml
services:
  disabled:
  - service_name: '{{ service_name }}'
  enabled:
  - service_name: '{{ service_name }}'
  timestamps:
  - modifiers: '{{ modifiers.split('' '') }}'
    type: '{{ type }}'

```
### snmp ifmib
```yaml
snmp:
  ifmib:
    ifindex:
      persist: true

```
### snmp-server location
```yaml
snmp:
  server:
    communities:
    - acl: '{{ acl }}'
      community: '{{ community }}'
      type: '{{ type }}'
    contact: '"{{ contact }}"'
    location: '"{{ location }}"'

```
### spanning-tree extend system-id
```yaml
spanning-tree:
  extend_system-id: true
  mode: '{{ mode }}'

```
### tacacs-server timeout
```yaml
tacacs_server:
  directed_request: true
  hosts:
  - ip: '{{ host }}'
  - encryption_type: '{{ encryption_type }}'
    ip: '{{ host }}'
    password: '{{ password }}'
  key:
    encryption_type: '{{ encryption_type }}'
    password: '{{ password }}'
  timeout: '{{ timeout }}'

```
### udld
```yaml
udld:
  enable: true

```
### username
```yaml
usernames:
- encryption_type: '{{ encryption_type }}'
  password: '{{ password }}'
  username: '{{ username }}'
- encryption_type: '{{ encryption_type }}'
  secret: '{{ secret }}'
  username: '{{ username }}'

```
### version
```yaml
version: '{{ version }}'

```
### svlan internal allocation policy
```yaml
vlan:
  internal_allocation_policy: '{{ direction }}'

```
### vrf
```yaml
vrfs:
  '{{ name }}':
    address_families:
      '{{ address_family }}':
        address_family: '{{ address_family }}'
    address_family_delimeter: bang
    address_family_exit_command: exit-address-family
    description: '{{ description }}'
    name: '{{ name }}'
    route_distinguisher:
      arbitrary_number: '{{ arbitrary_number }}'
      as: '{{ as }}'

```
