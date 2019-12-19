"""
--- Day 13: Care Package ---

https://adventofcode.com/2019/day/13

"""

import itertools
import collections

from dataclasses import dataclass

import _tools


def _get_param(data, param, mode, base):
    if mode == 0:
        return data[param]
    elif mode == 1:
        return param
    elif mode == 2:
        return data[param + base]

BLOCK_SYMBOL = '='


def run(code):
    data = code[:]
    data.extend([0] * 1000)

    # robot_pos = (0, 0)
    # # up, left, down, right
    # directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    # direction = 0
    # colors = collections.defaultdict(list)

    tile2draw = {
        0: '.',  # is an empty tile. No game object appears in this tile.
        1: 'X',  # is a wall tile. Walls are indestructible barriers.
        2: BLOCK_SYMBOL,  # is a block tile. Blocks can be broken by the ball.
        3: '-',  # is a horizontal paddle tile. The paddle is indestructible.
        4: 'o',  # is a ball tile. The ball moves diagonally and bounces off objects.
    }

    input_ = []
    output = []

    relative_base = 0
    pos = 0

    # input_.append(1)

    canvas = collections.defaultdict(str)
    _step = -1
    while True:
        # for d in data:
        #     print(d)
        if len(output) == 3:
            _step += 1
            print('_step', _step)

            x, y, tile_id = output
            print(output)
            draw_symbol = tile2draw[tile_id]
            _pos = (x, y)
            if _pos in canvas:
                a = 0
            canvas[_pos] = draw_symbol

            ys = [pos[1] for pos in canvas.keys()]
            xs = [pos[0] for pos in canvas.keys()]
            min_y, max_y = min(ys), max(ys)
            min_x, max_x = min(xs), max(xs)

            print('y from {} to {}'.format(min_y, max_y))
            print('x from {} to {}'.format(min_x, max_x))
            for _y in range(min_y, max_y + 1):
                line = [canvas.get((_x, _y), '.') for _x in range(min_x, max_x + 1)]
                print(''.join(line))
            output = []

        instruction = data[pos]
        instruction_str = f'{instruction:05d}'

        op_code = int(instruction_str[-2:])
        mode1 = int(instruction_str[-3])
        mode2 = int(instruction_str[-4])
        mode3 = int(instruction_str[-5])
        if mode3 == 2:
            pass

        if op_code == 1:
            op1, op2, op3 = data[pos + 1], data[pos + 2], data[pos + 3]
            op1, op2 = _get_param(data, op1, mode1, relative_base), _get_param(data, op2, mode2, relative_base)
            if mode3 == 2:
                op3 += relative_base

            data[op3] = op1 + op2

            pos += 4
        elif op_code == 2:
            op1, op2, op3 = data[pos + 1], data[pos + 2], data[pos + 3]
            op1, op2 = _get_param(data, op1, mode1, relative_base), _get_param(data, op2, mode2, relative_base)
            if mode3 == 2:
                op3 += relative_base

            data[op3] = op1 * op2

            pos += 4
        elif op_code == 3:
            op1 = data[pos + 1]
            if mode1 == 2:
                op1 += relative_base
            else:
                pass
                # op1 = _get_param(data, op1, mode1, relative_base)
            data[op1] = input_.pop()

            pos += 2

        elif op_code == 4:
            op1 = data[pos + 1]
            if mode1 == 2:
                op1 += relative_base
                op1 = data[op1]
            else:
                op1 = _get_param(data, op1, mode1, relative_base)

            output.append(op1)
            pos += 2

        elif op_code == 5:
            op1 = data[pos + 1]
            op1 = _get_param(data, op1, mode1, relative_base)
            if op1 != 0:
                op2 = data[pos + 2]
                op2 = _get_param(data, op2, mode2, relative_base)
                pos = op2
            else:
                pos += 3

        elif op_code == 6:
            op1 = data[pos + 1]
            op1 = _get_param(data, op1, mode1, relative_base)
            if op1 == 0:
                op2 = data[pos + 2]
                op2 = _get_param(data, op2, mode2, relative_base)
                pos = op2
            else:
                pos += 3

        elif op_code == 7:
            op1, op2, op3 = data[pos + 1], data[pos + 2], data[pos + 3]
            op1, op2 = _get_param(data, op1, mode1, relative_base), _get_param(data, op2, mode2, relative_base)

            if mode3 == 2:
                op3 += relative_base

            data[op3] = int(op1 < op2)

            pos += 4

        elif op_code == 8:
            op1, op2, op3 = data[pos + 1], data[pos + 2], data[pos + 3]
            op1, op2 = _get_param(data, op1, mode1, relative_base), _get_param(data, op2, mode2, relative_base)

            if mode3 == 2:
                op3 += relative_base

            data[op3] = int(op1 == op2)

            pos += 4

        elif op_code == 9:
            op1 = data[pos + 1]
            op1 = _get_param(data, op1, mode1, relative_base)
            relative_base += op1

            pos += 2

        elif op_code == 99:
            break
        else:
            # error
            print(f'bad opp code: pos {pos} op_code {op_code}')
            raise ValueError(f'bad opp code: pos {pos} op_code {op_code}')

    return canvas


def solve(data):
    data = list(data)
    canvas = run(data)

    blocks = 0
    for tile_symbol in canvas.values():
        if tile_symbol == BLOCK_SYMBOL:
            blocks += 1

    return blocks


def part1():
    data = _tools.get_puzzle_input()
    return solve(data)


if __name__ == '__main__':
    for res in (
        # test(1),
        part1(),
        # test(2),
        # test(3),
        # part2(),
    ):
        print(res)
