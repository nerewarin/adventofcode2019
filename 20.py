"""
--- Day 20: Donut Maze ---

https://adventofcode.com/2019/day/20

"""

import collections
import itertools

import _tools


class Tile:
    free = '.'
    wall = '#'


class DonutMaze:
    def __init__(self, inp=None, to_print=False):
        self.inp = inp or _tools.get_puzzle_input(scalar_type=str, multiline=True)
        self.to_print = to_print
        self._portals = {}
        self._maze, portal_parts = self._parse_maze_and_portals(inp)
        self._start, self._portals = self._parse_portal_parts(portal_parts)

    def _parse_maze_and_portals(self, inp):
        pos2symbol = collections.defaultdict(str)
        portal_parts = collections.defaultdict(list)
        for y, line in enumerate(inp):
            for x, symbol in enumerate(line):
                pos = x, y
                if symbol.isalpha() and symbol.isupper():
                    portal_parts[symbol].append(pos)

                pos2symbol[pos] = symbol

        return pos2symbol, portal_parts

    def _is_portal(self, x, y):
        return (x, y) in self._portals

    @staticmethod
    def _is_wall(symbol):
        return symbol == Tile.wall

    @staticmethod
    def _is_free(symbol):
        return symbol == Tile.free

    def _parse_portal_parts(self, portal_parts):
        portals = {}

        start_pos = None
        for portal, portal_poses in portal_parts.items():
            # every portal consists of two parts
            if len(portal_poses) != 2:
                raise ValueError(f'len(portal_poses) = {len(portal_poses)} for portal {portal}')

            portals[portal] = self._get_portal_exit(portal, portal_poses, portal_parts)

        for portal, portal_poses in portal_parts.items():
            first, second = portal_poses
            if first[0] == second[0]:
                common_x = first[0]
                assert abs(first[1] - second[1]) == 1
                centre_y = (first[1] + second[1]) / 2
                candidates = (
                    (common_x, centre_y - 1.5),
                    (common_x, centre_y + 1.5),
                )
            elif first[1] == second[1]:
                assert first[1] == second[1]
                common_y = first[1]
                assert abs(first[0] - second[0]) == 1
                centre_x = (first[0] + second[0]) / 2
                candidates = (
                    (centre_x - 1.5, common_y),
                    (centre_x + 1.5, common_y),
                )
            else:
                raise ValueError(f'portal_poses are not adjacent! {portal_poses}')

            for candidate in candidates:
                for adjacent_node in self._get_adjacent_nodes(candidate):
                    break
            else:
                raise ValueError()
            a = 9

    def _get_portal_exit(self, portal, portal_poses, portal_parts):
        if portal == 'A':

        # portal_parts has format 'A': [pos1, pos2]
        # lets group them by adjacency
        for adjacent_tile in self._get_adjacent_nodes(candidate):

    def _get_adjacent_nodes(self, vertex):
        for x, y in (
            (vertex[0], vertex[1] - 1),
            (vertex[0], vertex[1] + 1),
            (vertex[0] - 1, vertex[1]),
            (vertex[0] + 1, vertex[1]),
        ):
            symbol = self._maze[(x, y)]
            if not symbol:
                continue

            elif self._is_wall(symbol):
                continue

            elif self._is_free(symbol):
                yield x, y

            elif self._is_portal(x, y):
                raise NotImplementedError()

            yield symbol

    def get_shortest_path(self):
        start_level = 0
        queue = collections.deque([(self._start_pos, start_level, self._collected_keys)])
        seen = {
            (self._start_pos, tuple(self._collected_keys)): start_level
        }
        visit_order = []
        doors_locked = {}

        while queue:
            vertex, level, keys_collected = queue.popleft()
            visit_order.append((vertex, level, keys_collected))

            self._draw_maze(vertex, keys_collected)

            if self.is_complete(keys_collected):
                # all keys collected
                return vertex, level, keys_collected, doors_locked

            for x, y, door_or_keys in self._get_adjacent_nodes(vertex, keys_collected):
                if self._is_door(door_or_keys):
                    doors_locked[door_or_keys] = (x, y)
                    continue

                new_keys_collected = door_or_keys
                node = (x, y)
                if (node, new_keys_collected) in seen:
                    continue

                new_level = level + 1

                seen[(node, new_keys_collected)] = new_level

                queue.append(
                    (node, new_level, tuple(new_keys_collected))
                )

        # raise NoSolution()


def part1(*args, **kwargs):
    return DonutMaze(*args, **kwargs).get_shortest_path()


def part2():
    solver = DonutMaze()
    solver.simulate_recursively(200)
    return solver.count_all_bugs()


def _parse_input(inp):
    min_col_idx = float('inf')
    lines = [val for val in inp.split('\n') if val.strip()]
    for line in lines:
        for col_idx, symbol in enumerate(line):
            if symbol != ' ' and col_idx < min_col_idx:
                min_col_idx = col_idx

    return [[symbol for symbol in line[min_col_idx:]] for line in lines]


def test(test_num):
    if test_num == 1:
        _inp = '''
                     A           
                     A           
              #######.#########  
              #######.........#  
              #######.#######.#  
              #######.#######.#  
              #######.#######.#  
              #####  B    ###.#  
            BC...##  C    ###.#  
              ##.##       ###.#  
              ##...DE  F  ###.#  
              #####    G  ###.#  
              #########.#####.#  
            DE..#######...###.#  
              #.#########.###.#  
            FG..#########.....#  
              ###########.#####  
                         Z       
                         Z       
            '''
        expected = 23
    else:
        raise NotImplementedError(f'unknown test_num = {test_num}')

    inp = _parse_input(_inp)
    res = DonutMaze(inp, to_print=True).get_shortest_path()
    assert res == expected, 'test{} failed!: {}'.format(test_num, res)
    return 'test{} ok'.format(test_num)


if __name__ == '__main__':
    for res in (
        test(1),
        # test(2),
        # test(3),  # 108, 91
        # part1(),
        # part2(),  # 101 is low, 1748 and 2042 are wrong
    ):
        print(res)
