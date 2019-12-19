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


def get_puzzle_input():
    fpath = os.path.join('inputs', '{}.txt'.format(get_initiator_fname()))
    print('reading {}'.format(fpath))
    with open(fpath, 'r') as f:
        return [int(i) for i in f.readline().split(',')]
