"""
--- Day 20: Donut Maze ---

https://adventofcode.com/2019/day/20

"""

import collections

import _tools


class Tile:
    free = '.'
    wall = '#'
    entry_portal = 'A'
    exit_portal = 'Z'


class NoSolution(Exception):
    pass


class DonutMaze:
    def __init__(self, inp=None, to_print=False):
        if inp is None:
            with open(_tools.get_initiator_fname()) as f:
                inp = _parse_input(f.read())
        self.inp = inp
        self.to_print = to_print
        self._portals = {}
        self._maze, self._portal_parts = self._parse_maze_and_portals()
        self._start = self._get_start()

    def _parse_maze_and_portals(self):
        pos2symbol = {}
        portal_parts = collections.defaultdict(list)
        for y, line in enumerate(self.inp):
            for x, symbol in enumerate(line):
                pos = x, y
                if self._is_portal(symbol):
                    portal_parts[symbol].append(pos)

                pos2symbol[pos] = symbol

        return pos2symbol, portal_parts

    def _get_start(self):
        first, second = self._portal_parts[Tile.entry_portal]

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
            raise ValueError(f'portal_poses are not adjacent! {first}, {second}')

        for candidate in candidates:
            candidate = tuple(int(part) for part in candidate)
            if self._is_free(self._maze.get(candidate)):
                return candidate
        else:
            raise ValueError()

    @staticmethod
    def _is_portal(symbol):
        return symbol.isalpha() and symbol.isupper()

    @staticmethod
    def _is_wall(symbol):
        return symbol == Tile.wall

    @staticmethod
    def _is_free(symbol):
        return symbol == Tile.free

    def _get_adjacent_coordinates(self, vertex):
        for coords in (
            (vertex[0], vertex[1] - 1),
            (vertex[0], vertex[1] + 1),
            (vertex[0] - 1, vertex[1]),
            (vertex[0] + 1, vertex[1]),
        ):
            if coords in self._maze:
                yield coords

    def _get_portal_exit(self, first_portal_symbol, first_portal_part_pos, second_portal_symbol, second_portal_part_pos):
        if second_portal_symbol in self._portals:
            return self._portals[second_portal_symbol]

        # find pos of second portal part symbol
        symbol_poses = []
        _symbol_poses = [pos for pos in self._portal_parts[second_portal_symbol]]
        for pos in _symbol_poses:
            for adjacent_pos in self._get_adjacent_coordinates(pos):
                if adjacent_pos in (first_portal_part_pos, second_portal_part_pos):
                    continue
                if self._maze[adjacent_pos] == first_portal_symbol:
                    symbol_poses.append(adjacent_pos)
        if len(symbol_poses) > 2:
            raise RuntimeError('prog error')

        # find exit
        for exit_label_pos in symbol_poses:
            exit_portal_pos = None
            for adjacent_pos in self._get_adjacent_coordinates(exit_label_pos):
                symbol = self._maze[adjacent_pos]

                if self._is_free(symbol):
                    return adjacent_pos

                elif self._is_portal(symbol):
                    exit_portal_pos = adjacent_pos

            for adjacent_pos in self._get_adjacent_coordinates(exit_portal_pos):
                symbol = self._maze.get(adjacent_pos)
                if self._is_free(symbol):
                    return adjacent_pos
            else:
                raise ValueError()
        else:
            raise NoSolution()

    def _get_free_adjacent_nodes(self, vertex, use_portals=True):
        x0, y0 = vertex
        for adjacent_node in self._get_adjacent_coordinates(vertex):
            x, y = adjacent_node
            symbol = self._maze.get(adjacent_node)
            if not symbol:
                continue

            elif self._is_wall(symbol):
                continue

            elif self._is_free(symbol):
                yield adjacent_node

            elif self._is_portal(symbol):
                if not use_portals:
                    continue

                if symbol == Tile.entry_portal:
                    continue
                if symbol == Tile.exit_portal:
                    yield adjacent_node
                    continue
                second_portal_part_pos = (x0 + (x - x0) * 2, (y0 + (y - y0) * 2))
                second_portal_symbol = self._maze[second_portal_part_pos]
                yield self._get_portal_exit(symbol, adjacent_node, second_portal_symbol, second_portal_part_pos)

    def _is_complete(self, vertex):
        return self._maze[vertex] == 'Z'

    def get_shortest_path(self):
        start_level = 0
        queue = collections.deque([(self._start, start_level)])
        seen = {
            self._start: start_level
        }
        visit_order = []

        while queue:
            vertex, level = queue.popleft()
            visit_order.append((vertex, level))

            if self._is_complete(vertex):
                return level - 1

            for x, y in self._get_free_adjacent_nodes(vertex):
                node = (x, y)
                if node in seen:
                    continue

                new_level = level + 1

                seen[node] = new_level

                queue.append(
                    (node, new_level)
                )


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


def run(part_num, *args, **kwargs):
    if part_num == 1:
        res = DonutMaze(*args, **kwargs).get_shortest_path()
        expected = 498
    else:
        raise NotImplementedError(f'unknown part_num = {part_num}')
    assert res == expected,  'part{} failed!: {}'.format(part_num, res)
    return 'run{} = {}'.format(part_num, res)


if __name__ == '__main__':
    for _res in (
        test(1),
        run(1),
    ):
        print(_res)
