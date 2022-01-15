#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, Luca Elin Haneklau <git@luca.lsys.ac>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
---
module: utm_group

author:
    - Luca Elin Haneklau (@lucaelin)

short_description: create, update or destroy a group entry in Sophos UTM

description:
    - Create, update or destroy a group entry in SOPHOS UTM.
    - This module needs to have the REST Ability of the UTM to be activated.


options:
    name:
        type: str
        description:
          - The name of the object. Will be used to identify the entry
        required: true
    comment:
        type: str
        description:
          - An optional comment to add to the group object
    members:
        type: list
        elements: str
        required: true
        descript:
          - List of all group members
extends_documentation_fragment:
- community.general.utm

'''

EXAMPLES = """
- name: Create UTM group entry
  community.general.utm_group:
    utm_host: sophos.host.name
    utm_token: abcdefghijklmno1234
    name: TestGroup
    members:
      - REF_NetNetTestnetwor
    state: present

- name: Remove UTM group entry
  community.general.utm_group:
    utm_host: sophos.host.name
    utm_token: abcdefghijklmno1234
    name: TestGroup
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
        comment:
            description: The comment string
            type: str
        members:
            descript: List of all group members
            type: list
            elements: str
"""

from ansible_collections.community.general.plugins.module_utils.utm_utils import UTM, UTMModule
from ansible.module_utils.common.text.converters import to_native


def main():
    endpoint = "network/group"
    key_to_check_for_changes = ["comment", "members"]
    module = UTMModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            comment=dict(type='str', required=False, default="Created by ansible"),
            members=dict(type='list', required=False, elements='str'),
        )
    )
    try:
        UTM(module, endpoint, key_to_check_for_changes).execute()
    except Exception as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
