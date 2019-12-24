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
        # for y in range(max_y):
        max_y = 50
        x = 50
        sm = 0
        for y in range(max_x):
            computer = IntcodeComputer()
            computer.feed(x)
            computer.feed(y)
            # print(f'feed ({x}, {y})')
            value = next(computer)
            # print(f'received {res}')
            # _map[(x, y)] = value
            sm += value
        return sum(val for val in _map.values() if val)

    def find_closest_square_under_beam(self, expected_width, expected_high): # 4950286 is too low!!!!
        # x_in_row = 0
        #
        # _map = collections.defaultdict(int)
        #
        # # start_x = 0
        # x = 0
        # start_y = 0
        # y = start_y
        # on_row_start = True
        # while x_in_row < expected_width:
        #     computer = IntcodeComputer()
        #     computer.feed(x)
        #     computer.feed(y)
        #     # print(f'feed ({x}, {y})')
        #     value = next(computer)
        #     # print(f'received {value}')
        #     _map[(x, y)] = value
        #     if value:
        #         on_row_start = False
        #         x_in_row += 1
        #         x += 1
        #         continue
        #
        #     if on_row_start:
        #         x += 1
        #         x_in_row = 0
        #         continue
        #
        #     on_row_start = True
        #     y += 1
        #
        #     # x -= x_in_row
        #
        #     # check x=1 start on the next level down y(this+1) using start of x on the current level y(this)
        #     xshift = 0
        #     _x = x - x_in_row
        #     while not _x:
        #         computer = IntcodeComputer()
        #         next_x = _x + xshift
        #         computer.feed(next_x)
        #         computer.feed(y)
        #         value = next(computer)
        #         _map[(x, y)] = value
        #         if value == 0:
        #             xshift += 1
        #         else:
        #             _x = next_x
        #
        #     x = _x
        #
        # min_x = x - x_in_row
        # y_in_row = sum(int(_map.get((x - 100, y), 0)) for y in range(y - 100, y + 1))
        # if y_in_row < x_in_row:
        #     raise RuntimeError("startcomputing with x coordinate of 100y in a row instead!!")
        #
        # # result for inputs/19.txt
        # assert min_x == 495
        # assert y_in_row == 49
        # assert y == 286

        min_x = 495 * 2
        y_in_row = 49
        y = 286 * 2
        # y = min_x * 2

        # print(x)
        # print(y)
        # print(visit_order)
        # print(levels)
        min_y, max_y = y - 100, y + 500
        min_x, max_x = min_x - 125, min_x + 125
        # print(f'after: vertex {vertex} pos {parent_computer.pos} base {parent_computer.relative_base}')
        print('y from {} to {}'.format(min_y, max_y))
        print('x from {} to {}'.format(min_x, max_x))
        count_y = 0
        for _y in range(min_y, max_y + 1):
            line = []
            for _x in range(min_x, max_x + 1):
                computer = IntcodeComputer()
                computer.feed(_x)
                computer.feed(_y)
                # print(f'feed ({x}, {y})')
                value = next(computer)
                line.append(str(value))
            if '1' in line:
                count_y += 1
            print(''.join(line))
            if count_y >= 99:
                a = 9
        # end draw region

        a = 0
        # x = min_x
        # while y_in_row < expected_high:
        #     y += 1
        #     computer = IntcodeComputer()
        #     computer.feed(x)
        #     computer.feed(y)
        #     # print(f'feed ({x}, {y})')
        #     value = next(computer)
        #     if value:
        #         y_in_row += 1
        #     else:
        #         x += 1
        #         min_x += 1




def part1(*args, **kwargs):
    return TractorBeam(*args, **kwargs).count_ones(50, 50)


def part2(*args, **kwargs):
    return TractorBeam(*args, **kwargs).find_closest_square_under_beam(100, 100)


if __name__ == '__main__':
    assert part1() == 121

    # for res in (
    #     part2(),
    # ):
    #     print(res)
