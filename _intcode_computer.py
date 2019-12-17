import os
import re
import collections
import traceback

from typing import Iterator


def _get_initiator_fname():
    # define script that has called us - previous py filename from callstack
    for line in reversed(traceback.format_stack()):
        res = re.search(r'File.*"(.*)[\\\/](\d+).py', line)
        if res:
            return res.group(2)
    raise ValueError()


class IntcodeComputer(Iterator):
    def __init__(self, memory=None, signals=None):
        if memory is None:
            fname = _get_initiator_fname()
            with open(os.path.join('inputs', '{}.txt'.format(fname))) as f:
                memory = f.read()
        memory = [int(x) for x in memory.split(',')]

        self.signals = signals or []

        self.memory = collections.defaultdict(int)
        self.memory.update({
            idx: value for idx, value in enumerate(memory)
        })
        self.relative_base = 0
        self.gen = self.compute(gen_mode=True)

    def __next__(self):
        return next(self.gen)

    def feed(self, value):
        # feed the generator
        self.signals.append(value)

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

    def compute(self, gen_mode=False):
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
                    if out not in range(3):
                        # The repair droid can reply with any of the following status codes:
                        # 0: The repair droid hit a wall. Its position has not changed.
                        # 1: The repair droid has moved one step in the requested direction.
                        # 2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
                        raise ValueError('wrong output {}'.format(out))
                    if gen_mode:
                        yield out
                    else:
                        return out
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
