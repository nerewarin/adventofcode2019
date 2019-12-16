"""
--- Day 6: Universal Orbit Map ---

https://adventofcode.com/2019/day/6

"""

import os
import math
import re
import itertools

from dataclasses import dataclass
from typing import Tuple


class UniversalOrbitMap:
    def __init__(self, inp=None, mode=None):
        if inp is None:
            with open(os.path.join('inputs', '{}.txt'.format(__file__.split('/')[-1].split('.')[0]))) as f:
                inp = f.read()

        self.inp = [map(int, self.inp_rexp.match(moon).groups()) for moon in lines]

    def orbit_count_checksums(self):
        return self.get_direct_orbits() + self.get_indirect_orbits()

inp1 = """
    COM)B
    B)C
    C)D
    D)E
    E)F
    B)G
    G)H
    D)I
    E)J
    J)K
    K)L
"""

def test(test_num):
    if test_num == 1:
        res = UniversalOrbitMap(inp1).orbit_count_checksums()

        assert res == '84462026', 'test{} failed!: {}'.format(test_num, res)
    else:
        raise ValueError('test{} not implemented'.format(test_num))
    return 'test{} ok'.format(test_num)


def part1():
    return UniversalOrbitMap().orbit_count_checksums()


def part2():
    return FFT(mode=2).run(100)[:8]


if __name__ == '__main__':
    for res in (
        # test(1),
        part1(),
        # test(2),
        # part2(),
    ):
        print(res)
