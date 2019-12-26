"""
--- Day 17: Set and Forget ---

https://adventofcode.com/2019/day/17

"""

from _intcode_computer import ASCIICapableComputer


def part1(*args, **kwargs):
    return ASCIICapableComputer(*args, **kwargs).get_sum_of_the_alignment_parameters()


def part2(*args, **kwargs):
    return ASCIICapableComputer(*args, **kwargs).collect_dust()


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
        res = ASCIICapableComputer(test_inp).get_sum_of_the_alignment_parameters()
        assert res == 76, 'test{} failed!: {}'.format(test_num, res)
    else:
        raise NotImplementedError(f'unknown test_num = {test_num}')

    return 'test{} ok'.format(test_num)


if __name__ == '__main__':
    for res in (
        # test(1),
        # part1(),
        part2(memory_changes={0: 2}),
    ):
        print(res)
