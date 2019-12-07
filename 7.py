"""
https://adventofcode.com/2019/day/7
"""

import itertools


def intcode_computer(*inputs):
    _inputs = list(inputs)
    with open('inputs/7.txt') as f:
        inp = [int(x) for x in f.read().split(',')]
        # inp = [int(x) for x in '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'.split(',')]
        # inp = [int(x) for x in '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'.split(',')]

        def get_value(val_or_idx, mode):
            if mode == 0:
                idx = val_or_idx
                return inp[idx]

            val = val_or_idx
            return val

        curr_idx = 0
        while True:
            instruction = inp[curr_idx]

            op = instruction % 100

            _ins = instruction // 100
            mode1 = _ins % 10

            _ins = _ins // 10
            mode2 = _ins % 10

            _ins = _ins // 10
            mode3 = _ins % 10

            if op == 99:
                return inp[0]

            param1 = inp[curr_idx + 1]
            param2 = inp[curr_idx + 2]
            param3 = inp[curr_idx + 3]
            if op < 3:
                shift = 4
                if op == 1:
                    inp[param3] = get_value(param1, mode1) + get_value(param2, mode2)
                elif op == 2:
                    inp[param3] = get_value(param1, mode1) * get_value(param2, mode2)
            elif op < 5:
                shift = 2
                if op == 3:
                    # Opcode 3 takes a single integer as input and saves it to the position given by its only parameter
                    inp[param1] = int(_inputs.pop(0))
                elif op == 4:
                    out = inp[param1]
                    yield out
            elif op < 7:
                # jump-if-true
                if op == 5 and get_value(param1, mode1):
                    shift = get_value(param2, mode2) - curr_idx
                # jump-if-false
                elif op == 6 and not get_value(param1, mode1):
                    shift = get_value(param2, mode2) - curr_idx
                else:
                    shift = 3
            elif op < 9:
                # less than
                if op == 7 and get_value(param1, mode1) < get_value(param2, mode2):
                    _val = 1
                # equals
                elif op == 8 and get_value(param1, mode1) == get_value(param2, mode2):
                    _val = 1
                else:
                    _val = 0
                inp[param3] = _val
                shift = 4

            curr_idx += shift


def part1():
    max_res = float('-infinity')

    phases_combinations = itertools.permutations([0, 1, 2, 3, 4])
    for phases in phases_combinations:
        inputs = [0]
        for phase in phases:
            outputs = []
            for inp in inputs:
                for output in intcode_computer(phase, inp):
                    outputs.append(output)

            inputs = outputs

        max_res = max(max_res, max(inputs))

    return max_res

# def part2():
#     return calc()


for res in (
    part1(),
    # part2(),
):
    # print(res)
    print(res)