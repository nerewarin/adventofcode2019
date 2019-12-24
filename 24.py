"""
--- Day 24: Planet of Discord ---

https://adventofcode.com/2019/day/24

"""

import collections
import itertools

import _tools


class PlanetOfDiscord:
    _size = 5

    def __init__(self, inp=None):
        _inp = inp or _tools.get_puzzle_input(scalar_type=str, multiline=True)
        self._layouts_history = set()
        self._lvl2inp = {
            0: tuple(tuple(1 if val == '#' else 0 for val in row) for row in _inp)
        }

    def _get_layout(self, level=0):
        return self._lvl2inp[level]

    @staticmethod
    def _get_value(layout, x, y):
        if y < 0 or y >= len(layout):
            return 0
        row = layout[y]
        if x < 0 or x >= len(row):
            return 0
        return row[x]

    def count_adjacent_bugs(self, layout, x, y):
        res = sum((
            self._get_value(layout, x + 1, y),
            self._get_value(layout, x - 1, y),
            self._get_value(layout, x, y + 1),
            self._get_value(layout, x, y - 1),
        ))
        return res

    def get_map(self, level=0):
        _map = collections.defaultdict(int)
        for row_idx in range(self._size):
            for col_idx in range(self._size):
                layout = self._lvl2inp[level]
                _map[(col_idx, row_idx)] = layout[row_idx][col_idx]
        return _map

    def get_first_repeated_layout(self, level=0):
        layout = self._get_layout(level)
        while layout not in self._layouts_history:
            self._layouts_history.add(layout)
            # print(len(self.layouts))

            new_list = []
            for y in range(self._size):
                new_row = []
                for x in range(self._size):
                    adjacent_bugs = self.count_adjacent_bugs(layout, x, y)
                    current_val = layout[y][x]

                    if current_val:
                        new_val = adjacent_bugs == 1
                    else:
                        new_val = adjacent_bugs in (1, 2)

                    new_row.append(int(new_val))

                new_list.append(tuple(new_row))

            layout = tuple(new_list)
            self._lvl2inp[level] = layout

        return self._lvl2inp[level]

    def get_biodiversity_rating(self, layout):
        rating = 0
        worth = 1
        for i, val in enumerate(itertools.chain.from_iterable(layout)):
            if val:
                rating += worth
            worth *= 2
        return rating

    def get_biodiversity_rating_of_repeating_layout(self):
        layout = self.get_first_repeated_layout()
        return self.get_biodiversity_rating(layout)

    def simulate_recursively(self, minutes):
        min_l, max_l = 0, 0
        for minute in range(minutes):
            # consider we add two new layers every odd step (first, 3th, ...)
            if not minute % 2:
                min_l -= 1
                max_l += 1
                nulls_layout = tuple([tuple([0] * self._size) for x in range(self._size)])
                self._lvl2inp[min_l] = nulls_layout
                self._lvl2inp[max_l] = nulls_layout

            new_lvl2layout = {}
            for level, layout in self._lvl2inp.items():
                new_list = []
                for y in range(self._size):
                    new_row = []
                    for x in range(self._size):
                        adjacent_bugs = self.count_adjacent_bugs(layout, x, y)
                        current_val = layout[y][x]

                        if current_val:
                            new_val = adjacent_bugs == 1
                        else:
                            new_val = adjacent_bugs in (1, 2)

                        new_row.append(int(new_val))

                    new_list.append(tuple(new_row))

                new_lvl2layout[level] = tuple(new_list)

            self._lvl2inp = new_lvl2layout

        return None

    def count_all_bugs(self):
        bugs = 0
        for level, layout in self._lvl2inp.items():
            bugs_on_lvl = sum(itertools.chain.from_iterable(layout))
            bugs += bugs_on_lvl

        return bugs


def part1(*args, **kwargs):
    return PlanetOfDiscord(*args, **kwargs).get_biodiversity_rating_of_repeating_layout()


def part2():
    solver = PlanetOfDiscord()
    solver.simulate_recursively(200)
    return solver.count_all_bugs()


def test(test_num):
    inp = '''
        ....#
        #..#.
        #..##
        ..#..
        #....
    '''
    if test_num == 1:
        _inp = [val.strip() for val in inp.split('\n') if val.strip()]
        res = PlanetOfDiscord(inp=_inp).get_biodiversity_rating_of_repeating_layout()
        assert res == 2129920, 'test{} failed!: {}'.format(test_num, res)
    elif test_num == 2:
        res = part1()
        assert res == 25719471, 'test{} failed!: {}'.format(test_num, res)
    elif test_num == 3:
        solver = PlanetOfDiscord()
        solver.simulate_recursively(10)
        res = solver.count_all_bugs()
        assert res == 99, 'test{} failed!: {}'.format(test_num, res)
    else:
        raise NotImplementedError(f'unknown test_num = {test_num}')

    return 'test{} ok'.format(test_num)


if __name__ == '__main__':
    for res in (
        # test(1),
        # test(2),
        test(3),
        # part1(),
        # part2(),
    ):
        print(res)
