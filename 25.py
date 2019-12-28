"""
--- Day 25: Cryostasis ---

https://adventofcode.com/2019/day/25

"""

import re
import collections
import itertools
import warnings
import random
import math

import _tools
from _intcode_computer import ASCIICapableComputer


_regexp = re.compile(r'- ([\w ]+)')


class Cryostasis(ASCIICapableComputer):
    directions = {
        'north': 'south',
        'south': 'north',
        'east': 'west',
        'west': 'east',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_msg = None
        # self._doors = []
        # self._visited_doors = []
        self._map = []

    def _get_msg(self, *args, **kwargs):
        self.last_msg = super(Cryostasis, self)._get_msg(*args, **kwargs)
        return self.last_msg

    def _extract_info(self, s, msg=None):
        if msg is None:
            msg = self.last_msg

        if s not in msg:
            return []

        info = []
        for line in msg[msg.rfind(s) + len(s):].split('\n')[1:]:
            _res = _regexp.match(line)
            if not _res:
                break

            res = _res.group(1)
            if res in (
                'giant electromagnet',
                'escape pod',
                'infinite loop',
                'molten lava',
            ):
                warnings.warn(f'found {res!r} in {self.curr_place!r} but skip it!')
                continue

            info.append(res)
        #
        # info = [
        #     m for m in msg[msg.rfind(s) + len(s):msg.rfind('Command')].split('\n')
        #     if m
        # ]
        #
        # items = []
        # for _item in info:
        #
        #
        #     items.append(_res.group(1))
        return info

    def run(self):
        def _get_door():
            if any(door not in directions for door in doors):
                raise ValueError(f'wrong door parsed: {doors}')

            for door in sorted(doors, key=lambda door: directions[door] == last_move):

                if door not in place2moves[place]:
                    break
                if directions[door] == last_move:
                    break
            else:

                if place not in ('Hull Breach', 'Stables', 'Navigation'):
                    raise RuntimeError('no unique way')

            place2moves[place].add(door)
            return door

        def get_state(msg, place):
            try:
                _place = msg.split('==')[1].strip()
            except Exception as e:
                pass
            else:
                place = _place

            self.curr_place = place
            _d = msg[msg.rfind(place) + len(place) + 4:]
            description = _d[:_d.find('\n')]
            if 'Command?' not in msg:
                raise NotImplementedError(msg)

            items = self._extract_info('Items here:', msg)
            if any(item in directions for item in items):
                raise ValueError(f'wrong item parsed: {items}')
            if items:
                for item in items:
                    self.feed(f'take {item}')
                # take_msg = self._get_msg(to_print=True)

            self.feed('inv')
            inv_msg = self._get_msg(to_print=True)
            inv = self._extract_info('Items in your inventory:', inv_msg)

            doors = self._extract_info('Doors here lead:', msg[msg.index(place):])
            return place, description, items, inv, doors

        directions = self.directions
        step = 1
        last_move = None
        place = None
        place2moves = collections.defaultdict(set)
        msg = self._get_msg(to_print=True)
        inv = []
        # while len(inv) < 8 or place != 'Navigation':
        while len(inv) < 8 or place != 'Security Checkpoint':
            place, description, items, inv, doors = get_state(msg, place)
            if place == 'Security Checkpoint':
                a = 9

            if place == 'Science Lab':
            # if place == 'Engeneering':
                door = 'north'
            # elif place == 'Storage':
            #     door = 'north'
            # elif place == 'Navigation':
            #     door = 'north'
            # elif place == 'Stables':
            #     door = 'north'
            # elif place == 'Sick Bay':
            #     door = 'west'
            # elif place == 'Observatory':
            #     door = 'south'
            else:
                door = _get_door()
            place2moves[place].add(door)
            # door = _get_door()
            self.feed(door)
            last_move = door

            self._map.append({
                'place': place,
                'doors': doors,
                'move': door,
                'take': items,
                'inv': inv,
                'description': description,
            })

            step += 1

            msg = self._get_msg(to_print=True)
            if not msg:
                raise ValueError()

        default_msg = self._get_msg(to_print=True)
        prev_nav_doors = None
        nav_doors = None
        all_inv = list(inv)
        probes = math.factorial(len(all_inv)) * 2
        while msg == default_msg or nav_doors == prev_nav_doors:
            if not probes:
                raise ValueError()

            random.shuffle(inv)
            for i, item in enumerate(inv):
                self.feed(f'drop {item}', to_print=True)
                inv.pop(i)
                break
                # msg = self._get_msg(to_print=True)
                # if msg == default_msg:
                #     continue

            msg = self._get_msg(to_print=True)
            if self._get_msg(to_print=True):
                raise ValueError('win??')
            if not inv:
                for item in all_inv:
                    self.feed(f'take {item}')
                    inv.append(item)

                print('picked all items')
                probes -= 1
                print(f'probes left {probes}')
                continue


            if msg == f'''
You drop the {item}.

Command?
''':
                continue


            msg = self._get_msg(to_print=True)
            if msg:
                a = 9
                try:
                    place, description, items, inv, nav_doors = get_state(msg, place)
                except Exception as e:
                    place, description, items, inv, nav_doors = get_state(msg, place)

            print(f'step {step}')
            step += 1

        for place_info in self._map:
            import pprint
            pprint.pprint(place_info)

        a = 9

    def feed(self, value, to_print=None):
        if self._to_print_feed:
            print('>>>', end='')

        for x in str(value):
            super().feed(ord(x), to_print)

        super().feed(self._new_line)


def part1(*args, **kwargs):
    return Cryostasis(*args, **kwargs).run()


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
        # test(1),
        part1(),
    ):
        print(res)
