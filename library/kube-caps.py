#!/usr/bin/python

import subprocess
import re

def main():
    module = AnsibleModule(
        argument_spec = dict(
        ),
    )

    facts = {}
    facts['kube_node_via_api'] = True

    result = {}
    result['rc'] = 0
    result['changed'] = False
    result['ansible_facts'] = facts

    args = ("kubectl", "version", "-c")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()

    output = popen.stdout.read()
    match = re.search("Major:\"(\d+)\"", output)
    if not match:
        module.fail_json(msg="Major not found!")
    major = int(match.group(1))

    match = re.search("Minor:\"(\d+)(\.\d+)?\+?\"", output)
    if not match:
        module.fail_json(msg="Minor not found!")
    minor = int(match.group(1))

    if minor < 10:
        facts['kube_node_via_api'] = False

    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *
main()
