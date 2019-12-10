"""
--- Day 10: Monitoring Station ---

https://adventofcode.com/2019/day/10

"""

import os
import math


class MonitoringStation:
    BUSY = 1
    place2int = {
        '.': 0,  # EMPTY
        '#': 1,  # BUSY
    }

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

    @staticmethod
    def get_angle(x1, y1, x2, y2):
        return math.atan2(y2 - y1, x2 - x1)

    def get_visible_asteroids_count(self, x1, y1):
        checked_angles = set()
        counter = 0
        for y2, line2 in enumerate(self.map):
            for x2, place2 in enumerate(line2):
                # skip self
                if x1 == x2 and y1 == y2:
                    continue

                if not place2:
                    continue

                angle = self.get_angle(x1, y1, x2, y2)
                if angle in checked_angles:
                    continue

                counter += 1
                checked_angles.add(angle)

        return counter

    def get_visibility_map(self):
        visibility_map = []
        for y1, line1 in enumerate(self.map):
            visibility_line = []
            for x1, place1 in enumerate(line1):
                # place is empty - save 0 as a num of visible asteroids
                if not place1:
                    visibility_line.append(place1)
                    continue

                # count visible asteroids by finding angles to every visible point
                visible_asteroids = self.get_visible_asteroids_count(x1, y1)
                visibility_line.append(visible_asteroids)

            visibility_map.append(visibility_line)

        return visibility_map

    def find_best_place_and_count(self):
        visibility_map = self.get_visibility_map()
        x, y = (0, 0)
        max_vision = float('-inf')
        for y1, line1 in enumerate(visibility_map):
            for x1, value in enumerate(line1):
                if value > max_vision:
                    x, y = (x1, y1)
                    max_vision = value

        return (x, y), max_vision


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


def test2():
    inp = '''
        #.........
        ...A......
        ...B..a...
        .EDCG....a
        ..F.c.b...
        .....c....
        ..efd.c.gb
        .......c..
        ....f...c.
        ...e..d..c
    '''
    return 'test2 is not implemented'


def test3():
    inp = '''
        ......#.#.
        #..#.#....
        ..#######.
        .#.#.###..
        .#..#.....
        ..#....#.#
        #..#....#.
        .##.#..###
        ##...#..#.
        .#....####
    '''
    res = MonitoringStation(inp).find_best_place_and_count()
    assert res == ((5, 8), 33), 'test3 failed!: {}'.format(res)
    return 'test3 ok'


def test4():
    inp = '''
        #.#...#.#.
        .###....#.
        .#....#...
        ##.#.#.#.#
        ....#.#.#.
        .##..###.#
        ..#...##..
        ..##....##
        ......#...
        .####.###.
    '''
    res = MonitoringStation(inp).find_best_place_and_count()
    assert res == ((1, 2), 35), 'test4 failed!: {}'.format(res)
    return 'test4 ok'


def test5():
    test_num = 5
    inp = '''
        .#..#..###
        ####.###.#
        ....###.#.
        ..###.##.#
        ##.##.#.#.
        ....###..#
        ..#.#..#.#
        #..#.#.###
        .##...##.#
        .....#.#..
    '''
    res = MonitoringStation(inp).find_best_place_and_count()
    assert res == ((6, 3), 41), 'test{} failed!: {}'.format(test_num, res)
    return 'test{} ok'.format(test_num)


def part1(*args, **kwargs):
    return MonitoringStation(*args).find_best_place_and_count()


def part2(*args, **kwargs):
    return MonitoringStation(*args).find_best_place()


if __name__ == '__main__':
    for res in (
        test1(),
        test2(),
        test3(),
        test4(),
        test5(),
        part1(),
        # part2(),
    ):
        print(res)
