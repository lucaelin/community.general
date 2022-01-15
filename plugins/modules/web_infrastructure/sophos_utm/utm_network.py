#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Luca Elin Haneklau <git@luca.lsys.ac>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
---
module: utm_network

author:
    - Luca Elin Haneklau (@lucaelin)

short_description: create, update or destroy a network entry in Sophos UTM

description:
    - Create, update or destroy a network entry in SOPHOS UTM.
    - This module needs to have the REST Ability of the UTM to be activated.


options:
    name:
        type: str
        description:
          - The name of the object. Will be used to identify the entry
        required: true
    address:
        type: str
        description:
          - The IPV4 Address of the entry
    address6:
        type: str
        description:
          - The IPV6 Address of the entry
    netmask:
        type: int
        description:
          - The IPV4 Netmask of the entry
    netmask6:
        type: int
        description:
          - The IPV6 Netmask of the entry
    comment:
        type: str
        description:
          - An optional comment to add to the host object
    interface:
        type: str
        description:
          - The reference name of the interface to use. If not provided the default interface will be used
    resolved:
        description:
          - whether the hostname's ipv4 address is already resolved or not
        default: False
        type: bool
    resolved6:
        description:
          - whether the hostname's ipv6 address is already resolved or not
        default: False
        type: bool
    timeout:
        type: int
        description:
          - the timeout for the utm to resolve the ip address for the hostname again
        default: 0
extends_documentation_fragment:
- community.general.utm

'''

EXAMPLES = """
- name: Create UTM network entry
  community.general.utm_network:
    utm_host: sophos.host.name
    utm_token: abcdefghijklmno1234
    name: TestNetwork
    address: 1.2.3.0
    netmask: 24
    state: present

- name: Remove UTM network entry
  community.general.utm_network:
    utm_host: sophos.host.name
    utm_token: abcdefghijklmno1234
    name: TestNetwork
    state: absent
"""

RETURN = """
result:
    description: The utm object that was created
    returned: success
    type: complex
    contains:
        _ref:
            description: The reference name of the object
            type: str
        _locked:
            description: Whether or not the object is currently locked
            type: bool
        name:
            description: The name of the object
            type: str
        address:
            description: The ipv4 address of the object
            type: str
        address6:
            description: The ipv6 address of the object
            type: str
        netmask:
            type: int
            description:
              - The IPV4 Netmask of the entry
        netmask6:
            type: int
            description:
              - The IPV6 Netmask of the entry
        comment:
            description: The comment string
            type: str
        interface:
            description: The reference name of the interface the object is associated with
            type: str
"""

from ansible_collections.community.general.plugins.module_utils.utm_utils import UTM, UTMModule
from ansible.module_utils.common.text.converters import to_native


def main():
    endpoint = "network/network"
    key_to_check_for_changes = ["comment", "address", "address6", "netmask", "netmask6", "interface"]
    module = UTMModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            address=dict(type='str', required=False),
            address6=dict(type='str', required=False),
            netmask=dict(type='int', required=False),
            netmask6=dict(type='int', required=False),
            comment=dict(type='str', required=False, default="Created by ansible"),
            interface=dict(type='str', required=False),
            resolved=dict(type='bool', required=False),
            resolved6=dict(type='bool', required=False),
        )
    )
    try:
        UTM(module, endpoint, key_to_check_for_changes).execute()
    except Exception as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
