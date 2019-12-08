"""
--- Day 8: Space Image Format ---

https://adventofcode.com/2019/day/8
"""

import collections


class DigitalSendingNetwork:
    pass


def part1(inputs=None):
    if inputs is None:
        with open('inputs/8.txt') as f:
            inputs = [[int(symbol) for symbol in row] for row in f.read().split('\n')][0]

    layers_size = 25 * 6
    layers_amount = len(inputs) // layers_size

    layers = [inputs[layer * layers_size: (layer + 1) * layers_size] for layer in range(layers_amount)]

    counters = [collections.Counter(layer) for layer in layers]
    counter_idx, fewest_nulls = None, float('inf')
    for idx, counter in enumerate(counters):
        nulls = counter[0]
        if nulls < fewest_nulls:
            fewest_nulls = nulls
            counter_idx = idx

    counter = counters[counter_idx]
    return counter[1] * counter[2]


if __name__ == '__main__':
    for res in (
        part1(),
        # part2(),
    ):
        # print(res)
        print(res)
