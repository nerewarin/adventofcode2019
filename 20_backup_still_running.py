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
    def __init__(self, inp=None, to_print=False, recursive=False):
        if inp is None:
            with open(_tools.get_initiator_fname()) as f:
                inp = _parse_input(f.read())
        self.inp = inp
        self.to_print = to_print
        self._portals = {}
        self._maze, self._portal_parts = self._parse_maze_and_portals()
        self._start = self._get_start()
        self._recursive = recursive
        self._maze_width = len(self.inp[0])
        self._maze_height = len(self.inp)

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

    def _get_portal_exit(self, first_portal_symbol, first_portal_part_pos, second_portal_symbol, second_portal_part_pos, floor):
        portal_title = first_portal_symbol + second_portal_symbol
        if (first_portal_part_pos, floor) in self._portals:
            return self._portals[first_portal_part_pos]

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
        for exit_portal_part1 in symbol_poses:
            exit_portal_part2 = None
            for adjacent_pos in self._get_adjacent_coordinates(exit_portal_part1):
                symbol = self._maze[adjacent_pos]

                if self._is_free(symbol):
                    return adjacent_pos, self._get_next_floor(*adjacent_pos, floor, portal_title), portal_title

                elif self._is_portal(symbol):
                    exit_portal_part2 = adjacent_pos

            for adjacent_pos in self._get_adjacent_coordinates(exit_portal_part2):
                symbol = self._maze.get(adjacent_pos)
                if self._is_free(symbol):
                    # self._portals[(first_portal_part_pos, floor)] = adjacent_pos, next_floor
                    return adjacent_pos, self._get_next_floor(*adjacent_pos, floor, portal_title), portal_title
            else:
                raise ValueError()
        else:
            raise NoSolution()

    def _get_next_floor(self, x, y, floor, portal_double_symbol):
        if not self._recursive:
            shift = 0
        elif 2 < x < self._maze_width - 3 and 2 < y < self._maze_height - 3:
            shift = 1
        else:
            shift = -1
        # shift = 0
        return floor + shift

    def _get_free_adjacent_nodes(self, vertex, floor):
        x0, y0 = vertex
        for adjacent_node in self._get_adjacent_coordinates(vertex):
            x, y = adjacent_node
            symbol = self._maze.get(adjacent_node)
            if not symbol:
                continue

            elif self._is_wall(symbol):
                continue

            elif self._is_free(symbol):
                yield adjacent_node, floor, None

            elif self._is_portal(symbol):
                if symbol == Tile.entry_portal:
                    continue
                if symbol == Tile.exit_portal:
                    if not floor:
                        yield adjacent_node, floor, None
                    continue
                second_portal_part_pos = (x0 + (x - x0) * 2, (y0 + (y - y0) * 2))
                second_portal_symbol = self._maze[second_portal_part_pos]
                yield self._get_portal_exit(symbol, adjacent_node, second_portal_symbol, second_portal_part_pos, floor)

    def _is_complete(self, vertex):
        return self._maze[vertex] == 'Z'

    # def _get_state(self, node, new_level, floor):

    def get_shortest_path(self):
        start_level = 0
        start_floor = 0
        path = []
        queue = collections.deque([(self._start, start_level, start_floor, path)])
        seen = {
            (start_floor, self._start): start_level
        }
        # visit_order = [(start_level, start_floor, self._start)]

        while queue:
            vertex, level, floor, path = queue.popleft()

            if self._is_complete(vertex):
                for step in path:
                    if not step[-1]:
                        continue
                    print(step)
                return level - 1

            for xy, next_floor, portal_title in self._get_free_adjacent_nodes(vertex, floor):
                _path = list(path)
                if (next_floor, xy) in seen:
                    continue

                new_level = level + 1

                seen[(next_floor, xy)] = new_level

                # if next_floor != floor:
                # visit_order.append((level, floor, vertex))

                _path.append((vertex, floor, portal_title))

                queue.append(
                    (xy, new_level, next_floor, _path)
                )

        raise NoSolution()


def _parse_input(inp):
    min_col_idx = float('inf')
    lines = [val for val in inp.split('\n') if val.strip()]
    for line in lines:
        for col_idx, symbol in enumerate(line):
            if symbol != ' ' and col_idx < min_col_idx:
                min_col_idx = col_idx

    return [[symbol for symbol in line[min_col_idx:]] for line in lines]


def test(test_num, recursive=False):
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
        if recursive:
            expected = 26
        else:
            expected = 23
    else:
        raise NotImplementedError(f'unknown test_num = {test_num}')

    inp = _parse_input(_inp)
    res = DonutMaze(inp, to_print=True, recursive=recursive).get_shortest_path()
    assert res == expected, 'test{} failed!: {}'.format(test_num, res)
    return 'test{} {}ok'.format(test_num, '(recursice) ' if recursive else '')


def run(part_num, *args, **kwargs):
    if part_num == 1:
        res = DonutMaze(*args, **kwargs).get_shortest_path()
        expected = 498
    elif part_num == 2:
        res = DonutMaze(*args, recursive=True, **kwargs).get_shortest_path()
        expected = 'unknown'
        if res <= 508:
            raise ValueError('run{} = {}: answer is too low!'.format(part_num, res))
    else:
        raise NotImplementedError(f'unknown part_num = {part_num}')

    if expected != 'unknown':
        assert res == expected,  f'part{part_num} failed!: res = {res} but {expected} expected!'

    return 'run{} = {}'.format(part_num, res)


if __name__ == '__main__':
    for _res in (
        # test(1),
        # run(1),
        # test(1, recursive=True),
        run(2),
    ):
        print(_res)
