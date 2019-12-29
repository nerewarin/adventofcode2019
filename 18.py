"""
--- Day 18: Many-Worlds Interpretation ---

https://adventofcode.com/2019/day/18

"""

import re
import collections
import itertools
import warnings
import random
import math

import _tools


_regexp = re.compile(r'- ([\w ]+)')


class Tile:
    free = '.'
    agent = '@'


class MazeWithKeysAndDoors:
    def __init__(self, inp=None):
        self._maze, self._start_pos, self._doors, self._keys = self._parse_input_to_maze(inp)
        self._keys_collected = tuple()

    def _parse_input_to_maze(self, _inp):
        inp = _inp or _tools.get_puzzle_input(scalar_type=str, delimeter='', multiline=True)
        maze = []
        start_pos = None
        doors = {}
        keys = {}
        for row_num, line in enumerate(inp):
            row = []
            for col_num, symbol in enumerate(line):
                pos = (col_num, row_num)
                if self._is_door(symbol):
                    doors[symbol] = pos
                elif self._is_key(symbol):
                    keys[symbol] = pos
                elif self._is_agent(symbol):
                    start_pos = pos

                row.append(symbol)

            maze.append(row)

        return maze, start_pos, doors, keys

    @staticmethod
    def _is_wall(symbol):
        return symbol == '#'

    @staticmethod
    def _is_free(symbol):
        return symbol == Tile.free

    @staticmethod
    def _is_key(symbol):
        return symbol.isalpha() and symbol.islower()

    @staticmethod
    def _is_door(symbol):
        return symbol.isalpha() and symbol.isupper()

    @staticmethod
    def _is_agent(symbol):
        return symbol == Tile.agent

    def _draw_maze(self, vertex=None, keys=tuple()):
        if vertex is None:
            vertex = self._start_pos

        print()

        for row_num, line in enumerate(self._maze):
            for col_num, symbol in enumerate(line):
                if self._is_door(symbol) and self._door_is_open(symbol, keys):
                    symbol = Tile.free

                elif self._is_key(symbol) and symbol in keys:
                    symbol = Tile.free

                elif self._is_agent(symbol) and vertex != self._start_pos:
                    symbol = Tile.free

                elif (col_num, row_num) == vertex:
                    symbol = Tile.agent

                print(symbol, end='')

            print()

    def _get_symbol(self, x, y):
        try:
            return self._maze[y][x]
        except IndexError:
            return None

    @staticmethod
    def _door_is_open(door, keys_collected):
        return door.lower() in keys_collected

    def _get_adjacent_nodes(self, vertex, keys):
        for x, y in (
            (vertex[0], vertex[1] - 1),
            (vertex[0], vertex[1] + 1),
            (vertex[0] - 1, vertex[1]),
            (vertex[0] + 1, vertex[1]),
        ):
            symbol = self._get_symbol(x, y)
            if symbol is None:
                continue

            if self._is_wall(symbol):
                continue

            if self._is_free(symbol) or self._is_agent(symbol):
                yield x, y, keys

            elif self._is_door(symbol):
                if self._door_is_open(symbol, keys):
                    yield x, y, keys

            elif self._is_key(symbol):
                _keys = set(keys)
                yield x, y, tuple(_keys.union({symbol}))

    def get_shortest_path_of_collecting_all_keys(self):
        self._draw_maze()

        start_level = 0
        queue = collections.deque([(self._start_pos, start_level, self._keys_collected)])
        seen = {
            (self._start_pos, tuple(self._keys_collected)): start_level
        }
        visit_order = []

        while queue:
            vertex, level, keys_collected = queue.popleft()
            visit_order.append((vertex, level, keys_collected))

            # print(vertex, level, keys_collected)
            self._draw_maze(vertex, keys_collected)

            if len(keys_collected) == len(self._keys):
                return level

            for x, y, new_keys_collected in self._get_adjacent_nodes(vertex, keys_collected):
                # TODO
                node = (x, y)
                if (node, new_keys_collected) in seen:
                    continue

                new_level = level + 1

                seen[(node, new_keys_collected)] = new_level

                queue.append(
                    (node, new_level, tuple(new_keys_collected))
                )

        raise ValueError()


def part1(*args, **kwargs):
    return MazeWithKeysAndDoors(*args, **kwargs).get_shortest_path_of_collecting_all_keys()


def test(test_num):
    if test_num == 1:
        _inp = '''
            #########
            #b.A.@.a#
            #########
        '''
        expected = 8
    else:
        raise NotImplementedError(f'unknown test_num = {test_num}')

    inp = [val.strip() for val in _inp.split('\n') if val.strip()]
    # inp = None
    res = MazeWithKeysAndDoors(inp).get_shortest_path_of_collecting_all_keys()
    assert res == expected, 'test{} failed!: {}'.format(test_num, res)
    return 'test{} ok'.format(test_num)


if __name__ == '__main__':
    for res in (
        test(1),
        # part1(), # 536904736
    ):
        print(res)
