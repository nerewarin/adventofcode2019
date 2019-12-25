"""
--- Day 17: Set and Forget ---

https://adventofcode.com/2019/day/17

"""

from _intcode_computer import IntcodeComputer


class SetAndForget(IntcodeComputer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
    # test_inp = [val.strip() for val in _inp.split('\n') if val.strip()]
    test_inp = None
    if test_num == 1:
        res = SetAndForget(test_inp).compute()
        for r in res:
            symbol = chr(r)
            if symbol in '^v<>X':
                vacuum_robot_xy = symbol
            print(symbol, end='')
        print(f'vacuum_robot_xy: {vacuum_robot_xy}')
        # assert res == 2129920, 'test{} failed!: {}'.format(test_num, res)
    else:
        raise NotImplementedError(f'unknown test_num = {test_num}')

    return 'test{} ok'.format(test_num)


if __name__ == '__main__':
    for res in (
        test(1),
        # part1(),
    ):
        print(res)
