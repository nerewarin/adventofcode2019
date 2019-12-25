"""
--- Day 17: Set and Forget ---

https://adventofcode.com/2019/day/17

"""

from _intcode_computer import IntcodeComputer


class SetAndForget(IntcodeComputer):
    def __init__(self, _map=None):
        super().__init__()
        if _map:
            self._map = '\n'.join(_map)
        else:
            self._map = ''.join(chr(ascii_code) for ascii_code in self.compute())

    def _draw(self):
        for symbol in self._map:
            if symbol in '^v<>X':
                vacuum_robot_xy = symbol
            print(symbol, end='')
        print(f'\nvacuum_robot_xy: {vacuum_robot_xy}')

    @staticmethod
    def _get_value(layout, x, y):
        if y < 0 or y >= len(layout):
            return 0
        row = layout[y]
        if x < 0 or x >= len(row):
            return 0
        return row[x] == '#'

    def all_adjacent_are_scaffold(self, layout, x, y):
        return all((
            self._get_value(layout, x + 1, y),
            self._get_value(layout, x - 1, y),
            self._get_value(layout, x, y + 1),
            self._get_value(layout, x, y - 1),
        ))

    def get_sum_of_the_alignment_parameters(self):
        self._draw()
        layout = self._map.split('\n')
        alignments = []
        res = 0
        for y, row in enumerate(layout):
            for x, symbol in enumerate(row):
                if symbol == '#' and self.all_adjacent_are_scaffold(layout, x, y):
                    alignments.append((x, y))
                    res += x * y
        return res

def part1(*args, **kwargs):
    return SetAndForget(*args, **kwargs).get_sum_of_the_alignment_parameters()


def test(test_num):
    _inp = '''
        ..#..........
        ..#..........
        #######...###
        #.#...#...#.#
        #############
        ..#...#...#..
        ..#####...^..
    '''
    test_inp = [val.strip() for val in _inp.split('\n') if val.strip()]
    if test_num == 1:
        res = SetAndForget(test_inp).get_sum_of_the_alignment_parameters()
        assert res == 76, 'test{} failed!: {}'.format(test_num, res)
    else:
        raise NotImplementedError(f'unknown test_num = {test_num}')

    return 'test{} ok'.format(test_num)


if __name__ == '__main__':
    for res in (
        test(1),
        part1(),
    ):
        print(res)
