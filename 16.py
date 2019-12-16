"""
--- Day 16: Flawed Frequency Transmission ---

https://adventofcode.com/2019/day/16

"""

import os
import math
import re
import itertools

from dataclasses import dataclass
from typing import Tuple


class FFT:
    def __init__(self, inp=None):
        if inp is None:
            with open(os.path.join('inputs', '{}.txt'.format(__file__.split('/')[-1].split('.')[0]))) as f:
                inp = f.read()

        self.inp = [int(digit) for digit in inp.strip()]
        self.input_len = len(inp)
        self.pattern = [0, 1, 0, -1]
        self.pattern_len = len(self.pattern)

    def run(self, phases):
        inp = self.inp
        for phase in range(phases):
            new = []
            for idx in range(self.input_len):
                _pattern = [x for item in self.pattern for x in itertools.repeat(item, idx + 1)]
                _extend = int(math.ceil(self.input_len / len(_pattern)) + 1)
                pattern = (_pattern * _extend)[1: self.input_len + 1]

                if len(pattern) != self.input_len:
                    raise RuntimeError('len(pattern)', len(pattern))

                new_val = 0
                for idx2, value2 in enumerate(inp):
                    a = value2
                    b = pattern[idx2]
                    _new_val_part = a * b
                    new_val += _new_val_part

                val = abs(new_val) % 10
                new.append(val)

            # print(new)
            inp = new

        return ''.join(str(digit) for digit in inp)

inp = '12345678'


def test(test_num):
    if test_num == 1:
        res = FFT(inp).run(4)
        assert res == '01029498', 'test{} failed!: {}'.format(test_num, res)
    return 'test{} ok'.format(test_num)


def part1():
    return FFT().run(100)[:8]



if __name__ == '__main__':
    for res in (
        test(1),
        # part1(),
        # test(2),
        # part2(),
    ):
        print(res)
