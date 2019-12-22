import os
import re
import traceback


def get_initiator_fname():
    # define script that has called us - previous py filename from callstack
    for line in reversed(traceback.format_stack()):
        res = re.search(r'File.*"(.*)[\\\/](\d+).py', line)
        if res:
            return res.group(2)
    raise ValueError()


def get_puzzle_input(scalar_type=int, delimeter=',', multiline=False):
    fpath = os.path.join('inputs', '{}.txt'.format(get_initiator_fname()))
    print('reading {}'.format(fpath))
    with open(fpath, 'r') as f:
        if not multiline:
            return [scalar_type(i.strip()) for i in f.readline().split(delimeter)]
        return [scalar_type(i.strip()) for i in f.readlines()]
