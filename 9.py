"""
--- Day 9: Sensor Boost ---

https://adventofcode.com/2019/day/3
"""

import os
import collections


class intcodeComputer:
    def __init__(self, memory=None, signals=None):
        if memory is None:
            with open(os.path.join('inputs', '{}.txt'.format(__file__.split('/')[-1].split('.')[0]))) as f:
                memory = f.read()
        # self.memory = Memory([int(x) for x in memory.split(',')])
        memory = [int(x) for x in memory.split(',')]

        self.signals = signals or []

        self.memory = collections.defaultdict(int)
        self.memory.update({
            idx: value for idx, value in enumerate(memory)
        })
        self.relative_base = 0

    def get_value(self, val_or_idx, mode):
        if mode == 0:
            idx = val_or_idx
            if idx < 0:
                raise ValueError("idx {} cannot be negative!".format(mode))
            return self.memory[idx]
        elif mode == 1:
            val = val_or_idx
            return val
        elif mode == 2:
            idx = self.relative_base + val_or_idx
            if idx < 0:
                raise ValueError("idx {} cannot be negative!".format(mode))
            return self.memory[idx]
        else:
            raise ValueError("mode {} is unknown".format(mode))

    def get_write_idx(self, param, mode):
        if mode == 0:
            return param
        elif mode == 1:
            raise ValueError("mode {} is wrong for write mode!".format(mode))
        elif mode == 2:
            return param + self.relative_base
        else:
            raise ValueError("mode {} is unknown".format(mode))

    def compute(self):
        curr_idx = 0
        while True:
            instruction = self.memory[curr_idx]

            op = instruction % 100

            _ins = instruction // 100
            mode1 = _ins % 10

            _ins = _ins // 10
            mode2 = _ins % 10

            _ins = _ins // 10
            mode3 = _ins % 10

            if op == 99:
                return self.memory[0]

            param1 = self.memory[curr_idx + 1]
            param2 = self.memory[curr_idx + 2]
            try:
                param3 = self.memory[curr_idx + 3]
            except KeyError:
                param3 = None  # dirty but who cares

            if op < 3:
                shift = 4
                idx = self.get_write_idx(param3, mode3)
                if op == 1:
                    self.memory[idx] = self.get_value(param1, mode1) + self.get_value(param2, mode2)
                elif op == 2:
                    self.memory[idx] = self.get_value(param1, mode1) * self.get_value(param2, mode2)
            elif op < 5:
                shift = 2
                if op == 3:
                    # Opcode 3 takes a single integer as input and saves it to the position given by its only parameter
                    # idx = self.relative_base + param1
                    # idx = self.get_value(param1, mode1)
                    # idx = param1
                    idx = self.get_write_idx(param3, mode3)
                    if self.signals:
                        signal = self.signals.pop(0)
                    else:
                        signal = int(input('input:'))
                    self.memory[idx] = signal
                elif op == 4:
                    out = self.get_value(param1, mode1)
                    print(out)
            elif op < 7:
                # jump-if-true
                if op == 5 and self.get_value(param1, mode1):
                    shift = self.get_value(param2, mode2) - curr_idx
                # jump-if-false
                elif op == 6 and not self.get_value(param1, mode1):
                    shift = self.get_value(param2, mode2) - curr_idx
                else:
                    shift = 3
            elif op < 9:
                # less than
                if op == 7 and self.get_value(param1, mode1) < self.get_value(param2, mode2):
                    _val = 1
                # equals
                elif op == 8 and self.get_value(param1, mode1) == self.get_value(param2, mode2):
                    _val = 1
                else:
                    _val = 0
                idx = self.get_write_idx(param3, mode3)
                self.memory[idx] = _val
                shift = 4
            elif op == 9:
                # Opcode 9 adjusts the relative base by the value of its only parameter
                self.relative_base += self.get_value(param1, mode1)
                shift = 2
            else:
                raise NotImplemented("op={} is unknown".format(op))

            curr_idx += shift


def part1(*args, **kwargs):
    return intcodeComputer(*args, signals=[1], **kwargs).compute()


def part2(*args, **kwargs):
    return intcodeComputer(*args, signals=[2], **kwargs).compute()


if __name__ == '__main__':
    tst_mem1 = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    tst_mem2 = '1102,34915192,34915192,7,4,7,99,0'
    tst_mem3 = '104,1125899906842624,99'
    for res in (
        # part1(tst_mem1),
        # part1(tst_mem2),
        # part1(tst_mem3),
        part1(),
        part2(),
    ):
        # print(res)
        pass