#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Luca Elin Haneklau <git@luca.lsys.ac>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
---
module: utm_host

author:
    - Luca Elin Haneklau (@lucaelin)

short_description: create, update or destroy host entry in Sophos UTM

description:
    - Create, update or destroy a host entry in SOPHOS UTM.
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
    hostname:
        type: str
        description:
          - The hostname for the host object
    comment:
        type: str
        description:
          - An optional comment to add to the host object
    interface:
        type: str
        description:
          - The reference name of the interface to use. If not provided the default interface will be used
    duids:
        type: list
        elements: str
        description:
          - A list of DHCP unique identifiers to serve this address to
    reverse_dns:
        type: bool
        description:
          - Create a reverse dns entry for this IP
    macs:
        type: list
        elements: str
        description:
          - A list of mac address to serve this address to
    timeout:
        type: int
        description:
          - the timeout for the utm to resolve the ip address for the hostname again
        default: 0
extends_documentation_fragment:
- community.general.utm

'''

EXAMPLES = """
- name: Create UTM host entry
  community.general.utm_host:
    utm_host: sophos.host.name
    utm_token: abcdefghijklmno1234
    name: TestHostEntry
    address: 1.2.3.4
    state: present

- name: Remove UTM host entry
  community.general.utm_host:
    utm_host: sophos.host.name
    utm_token: abcdefghijklmno1234
    name: TestHostEntry
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
        hostname:
            type: str
            description: The hostname for the host object
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
    endpoint = "network/host"
    key_to_check_for_changes = ["comment", "address", "address6", "duids", "hostnames", "reverse_dns", "interface", "macs"]
    module = UTMModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            address=dict(type='str', required=False, default=''),
            address6=dict(type='str', required=False, default=''),
            comment=dict(type='str', required=False, default="Created by ansible"),
            duids=dict(type='list', required=False, elements='str', default=[]),
            hostnames=dict(type='list', required=False, elements='str', default=[]),
            reverse_dns=dict(type='bool', required=False, default=False),
            interface=dict(type='str', required=False, default=''),
            macs=dict(type='list', required=False, elements='str', default=[]),
            resolved=dict(type='bool', required=False),
            resolved6=dict(type='bool', required=False),
            timeout=dict(type='int', required=False)
        )
    )
    try:
        utm = UTM(module, endpoint, key_to_check_for_changes)
        if utm.module.params.get("resolved") == None:
            utm.module.params["resolved"] = utm.module.params.get("address") != ''
        if utm.module.params.get("resolved6") == None:
            utm.module.params["resolved6"] = utm.module.params.get("address6") != ''
        utm.execute()
    except Exception as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
