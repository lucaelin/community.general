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

short_description: add or delete members to group entry in Sophos UTM

description:
    - Add or delete members to group entry in Sophos UTM
    - This module needs to have the REST Ability of the UTM to be activated.


options:
    name:
        type: str
        description:
          - The name of the object. Will be used to identify the entry
        required: true
    members:
        type: list
        elements: str
        required: true
        descript:
          - List of all group members to add or delete
extends_documentation_fragment:
- community.general.utm

'''

EXAMPLES = """
- name: Add members to UTM group
  community.general.utm_group_members:
    utm_host: sophos.host.name
    utm_token: abcdefghijklmno1234
    name: TestGroup
    members:
      - REF_NetNetTestnetwor
    state: present

- name: Remove members from UTM group
  community.general.utm_group_members:
    utm_host: sophos.host.name
    utm_token: abcdefghijklmno1234
    name: TestGroup
    members:
      - REF_NetNetTestnetwor
    state: absent
"""

RETURN = """
result:
    description: The utm group object that was modified
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
            comment=dict(type='str', required=False, default="Modified by ansible"),
            members=dict(type='list', required=False, elements='str'),
        )
    )
    try:
        utm = UTM(module, endpoint, key_to_check_for_changes)
        info, result = utm.lookup_entry(utm.module, utm.request_url)
        current = result.get("members")
        target = utm.module.params.get("members")
        if (utm.module.params.get("state") == 'present'):
            for t in target:
                if t not in current:
                    current.append(t)
        if (utm.module.params.get("state") == 'absent'):
            for t in target:
                if t in current:
                    current.remove(t)

        comment = utm.module.params["comment"]
        if comment == utm.module.argument_spec["comment"]["default"]:
            utm.module.params["comment"] = result.get("comment")
        utm.module.params["members"] = current
        utm.module.params["state"] = 'present'
        utm.execute()
    except Exception as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
