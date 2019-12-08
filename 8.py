"""
--- Day 8: Space Image Format ---

https://adventofcode.com/2019/day/8
"""

import collections


class DigitalSendingNetwork:
    def __init__(self):
        with open('inputs/8.txt') as f:
            inputs = [[int(symbol) for symbol in row] for row in f.read().split('\n')][0]

        self.wide = 25
        self.tall = 6

        layers_size = self.wide * self.tall
        self.layers_size = layers_size

        layers_amount = len(inputs) // layers_size

        self.layers = [inputs[layer * layers_size: (layer + 1) * layers_size] for layer in range(layers_amount)]

    def calc_part1(self):
        counters = [collections.Counter(layer) for layer in self.layers]
        counter_idx, fewest_nulls = None, float('inf')
        for idx, counter in enumerate(counters):
            nulls = counter[0]
            if nulls < fewest_nulls:
                fewest_nulls = nulls
                counter_idx = idx

        counter = counters[counter_idx]
        return counter[1] * counter[2]

    def draw(self):
        black, white, transparent = range(3)
        # result = [[transparent for dummy_col in range(self.wide)] for dummy_row in range(self.tall)]
        result = [transparent for x in range(self.layers_size)]
        for layer in self.layers:
            for idx, color in enumerate(layer):
                if result[idx] is transparent:
                    result[idx] = color

        code2color = {
            black: '#',
            # black: ' ',
            # black: u"\u2588",
            # white: u"\u2B1C",
            white: ' ',
            # white: '#',
            # white: u"\u25AF",
            transparent: ''
        }
        res_str = ''
        res_str2 = ''
        for row in range(self.tall):
            for col in range(self.wide):
                cell_code = result[row * self.tall + col]
                color = code2color[cell_code]
                res_str += color
                res_str2 += str(cell_code)
            res_str += '\n'
            res_str2 += '\n'
        print(res_str2)
        return res_str


def part1():
    return DigitalSendingNetwork().calc_part1()


def part2():
    return DigitalSendingNetwork().draw()


if __name__ == '__main__':
    for res in (
        # part1(),
        part2(),
    ):
        print(res)
