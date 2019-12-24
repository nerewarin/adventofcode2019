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
        self.inp = tuple(tuple(1 if val == '#' else 0 for val in row) for row in _inp)
        self.layouts = set()

    @property
    def map(self):
        _map = collections.defaultdict(int)
        for row_idx in range(self._size):
            for col_idx in range(self._size):
                _map[(col_idx, row_idx)] = self.inp[row_idx][col_idx]
        return _map

    def count_adjacent_bugs(self, x, y):
        return sum((
            self.map[(x+1, y)],
            self.map[(x-1, y)],
            self.map[(x, y+1)],
            self.map[(x, y-1)],
        ))

    def get_first_repeated_layout(self):
        while self.inp not in self.layouts:
            self.layouts.add(self.inp)
            # print(len(self.layouts))

            new_list = []
            for y in range(self._size):
                new_row = []
                for x in range(self._size):
                    adjacent_bugs = self.count_adjacent_bugs(x, y)
                    current_val = self.inp[y][x]

                    if current_val:
                        new_val = adjacent_bugs == 1
                    else:
                        new_val = adjacent_bugs in (1, 2)

                    new_row.append(int(new_val))

                new_list.append(tuple(new_row))

            self.inp = tuple(new_list)

        return self.inp

    def get_biodiversity_rating(self):
        rating = 0
        worth = 1
        for i, val in enumerate(itertools.chain.from_iterable(self.inp)):
            if val:
                rating += worth
            worth *= 2
        return rating

    def get_biodiversity_rating_of_repeating_layout(self):
        self.get_first_repeated_layout()
        return self.get_biodiversity_rating()


def part1(*args, **kwargs):
    return PlanetOfDiscord(*args, **kwargs).get_biodiversity_rating_of_repeating_layout()


def test(test_num):
    if test_num == 1:
        inp = '''
            ....#
            #..#.
            #..##
            ..#..
            #....
        '''
        _inp = [val.strip() for val in inp.split('\n') if val.strip()]
        assert PlanetOfDiscord(inp=_inp).get_biodiversity_rating_of_repeating_layout() == 2129920, \
            'test{} failed!: {}'.format(test_num, res)
    else:
        raise NotImplementedError(f'unknown test_num = {test_num}')

    return 'test{} ok'.format(test_num)


if __name__ == '__main__':
    for res in (
        test(1),
        part1(),
    ):
        print(res)
