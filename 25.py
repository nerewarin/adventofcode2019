"""
--- Day 25: Cryostasis ---

https://adventofcode.com/2019/day/25

"""

import collections
import itertools

import _tools


class Cryostasis:
    def __init__(self, inp=None):
        _inp = inp or _tools.get_puzzle_input(scalar_type=str, multiline=True)

    def _draw(self):
        print(f'\n=== MINUTE {self.minute} ===\n')
        for level, layout in self._lvl2inp.items():
            # DRAW
            print('level', level)
            for row in layout:
                print(row)
            # END DRAW


def part1(*args, **kwargs):
    return Cryostasis(*args, **kwargs).get_biodiversity_rating_of_repeating_layout()


def test(test_num):
    _inp = '''
        ....#
        #..#.
        #..##
        ..#..
        #....
    '''
    test_inp = [val.strip() for val in _inp.split('\n') if val.strip()]
    if test_num == 1:
        res = Cryostasis(test_inp).get_biodiversity_rating_of_repeating_layout()
        assert res == 2129920, 'test{} failed!: {}'.format(test_num, res)
    else:
        raise NotImplementedError(f'unknown test_num = {test_num}')

    return 'test{} ok'.format(test_num)


if __name__ == '__main__':
    for res in (
        test(1),
        part1(),
    ):
        print(res)
