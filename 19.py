"""
--- Day 19: Tractor Beam ---

https://adventofcode.com/2019/day/19

"""

import collections

from _intcode_computer import IntcodeComputer


class TractorBeam:
    def __init__(self, *args, network_size=50, **kwargs):
        pass

    def count_ones(self, max_x, max_y):
        _map = collections.defaultdict(int)
        for y in range(max_y):
            for x in range(max_x):
                computer = IntcodeComputer()
                computer.feed(x)
                computer.feed(y)
                print(f'feed ({x}, {y})')
                res = next(computer)
                print(f'received {res}')
                _map[(x, y)] = res

        return sum(val for val in _map.values() if val)


def part1(*args, **kwargs):
    return TractorBeam(*args, **kwargs).count_ones(50, 50)


if __name__ == '__main__':
    for res in (
        part1(),
    ):
        print(res)
