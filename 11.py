"""
--- Day 10: Monitoring Station ---

https://adventofcode.com/2019/day/10

"""

import os
import math


class MonitoringStation:
    def __init__(self, _map=None):
        if _map is None:
            with open(os.path.join('inputs', '{}.txt'.format(__file__.split('/')[-1].split('.')[0]))) as f:
                _map = f.read()
        else:
            _map = '\n'.join((
                line.strip() for line in _map.split('\n')
            ))
        _map = [
            [self.place2int.get(place, self.BUSY) for place in line]
            for line in _map.split('\n') if line
        ]

        self.map = _map



def test1():
    inp = '''
        .#..#
        .....
        #####
        ....#
        ...##
    '''
    res = MonitoringStation(inp).get_visibility_map()
    assert res == [[0, 7, 0, 0, 7], [0, 0, 0, 0, 0], [6, 7, 7, 7, 5], [0, 0, 0, 0, 7], [0, 0, 0, 8, 7]], \
        'test1 failed!: {}'.format(res)
    return 'test1 ok'


def test7():
    test_num = 7
    res = MonitoringStation(inp6).vaporize(200)
    assert res == (8, 2), 'test{} failed!: {}'.format(test_num, res)
    return 'test{} ok'.format(test_num)


def part1(*args, **kwargs):
    return MonitoringStation(*args).find_best_place_and_count()
#
#
# def part2(*args, **kwargs):
#     x, y = MonitoringStation(*args).vaporize(200)
#     return x * 100 + y


if __name__ == '__main__':
    for res in (
        test1(),
        # test2(),
        # test3(),
        # test4(),
        # test5(),
        # test6(),
        # part1(),
        # test7(),
        # part2(),
    ):
        print(res)
