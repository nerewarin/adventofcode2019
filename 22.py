"""
--- Day 22: Slam Shuffle ---

https://adventofcode.com/2019/day/22

"""

import re
import collections

import _tools


class SlamShuffle:
    _increment_rexp = re.compile(r'deal with increment ([-]*\d+)')
    _cut_rexp = re.compile(r'cut ([-]*\d+)')

    def __init__(self, inp=None, deck_size=10007, deck=None):
        if inp is None:
            inp = _tools.get_puzzle_input(scalar_type=str, delimeter='\n', multiline=True)
        else:
            inp = [val.strip() for val in inp.split('\n') if val.strip()]
        self.inp = inp
        self._deck_size = deck_size
        self.deck = deck or list(range(self._deck_size))

    def _deal_with_increment(self, period):
        temp = collections.defaultdict(int)
        temp_idx = 0
        deck_idx = 0
        while deck_idx < self._deck_size:
            temp[temp_idx] = self.deck[deck_idx]
            temp_idx = (temp_idx + period) % self._deck_size
            deck_idx += 1
        self.deck = [temp[idx] for idx in range(self._deck_size)]

    def _shuffle(self):
        _last_instruction = None
        for instr_idx, raw_instruction in enumerate(self.inp):
            if len(set(self.deck)) != self._deck_size:
                raise ValueError(f'error dealing {_last_instruction}')
            if raw_instruction == 'deal into new stack':
                self.deck = self.deck[::-1]
                _last_instruction = raw_instruction
                continue

            _incr_instruction = self._increment_rexp.match(raw_instruction)
            if _incr_instruction:
                period = int(_incr_instruction.group(1))
                self._deal_with_increment(period)
                _last_instruction = raw_instruction
                continue

            _cut_instruction = self._cut_rexp.match(raw_instruction)
            if _cut_instruction:
                idx = int(_cut_instruction.group(1))
                self.deck = self.deck[idx:] + self.deck[:idx]
                _last_instruction = raw_instruction
                continue

            raise ValueError(f'unknown {raw_instruction}')
        return

    def get_position(self, value):
        f"""
        
        Args:
            value (int): value in deck (from 0 to 10006) 

        Returns:
            int: position of {value} in deck
            
        """
        self._shuffle()
        return self.deck.index(value)

    @staticmethod
    def _get_inct_pos(period, position, deck_size):
        if position == 0:
            return 0
        return (period * position - 1) % deck_size

    def reverse_shuffle(self, position, deck_size):
        # keep track of changing value in individual position
        original = position
        _last_instruction = None
        for instr_idx, raw_instruction in enumerate(self.inp):
            print(f'{position}: {raw_instruction}')
            if raw_instruction == 'deal into new stack':
                position = (-position - 1) % deck_size
                continue

            _incr_instruction = self._increment_rexp.match(raw_instruction)
            if _incr_instruction:
                period = int(_incr_instruction.group(1))

                # full_period = _tools.lcm(period, deck_size)
                if position != 0:
                    new_position = position
                    steps = 1
                    while True:
                        old_position, rest = divmod(new_position,  period)
                        if rest:
                            new_position += deck_size
                        else:
                            break
                        steps += 1
                    position = old_position

                _last_instruction = raw_instruction
                continue

            _cut_instruction = self._cut_rexp.match(raw_instruction)
            if _cut_instruction:
                idx = int(_cut_instruction.group(1))

                _idx = idx % deck_size
                position = (position - idx) % deck_size

                assert position < deck_size
                _last_instruction = raw_instruction
                continue

            raise ValueError(f'unknown {raw_instruction}')
        return position


def _str_to_deck(s):
    return [int(x) for x in s.split(' ')]


def test1():
    ss1 = SlamShuffle('''
        deal with increment 7
        deal into new stack
        deal into new stack
    ''', deck_size=10)
    ss1._shuffle()
    assert ss1.deck == _str_to_deck('0 3 6 9 2 5 8 1 4 7')

    ss2 = SlamShuffle('''
        cut 6
        deal with increment 7
        deal into new stack
    ''', deck_size=10)
    ss2._shuffle()
    assert ss2.deck == _str_to_deck('3 0 7 4 1 8 5 2 9 6')

    ss3 = SlamShuffle('''
deal with increment 7
deal with increment 9
cut -2
    ''', deck_size=10)
    ss3._shuffle()
    assert ss3.deck == _str_to_deck('6 3 0 7 4 1 8 5 2 9')

    ss4 = SlamShuffle('''
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
    ''', deck_size=10)
    ss4._shuffle()
    assert ss4.deck == _str_to_deck('9 2 5 8 1 4 7 0 3 6')


def part1(*args, **kwargs):
    return SlamShuffle(*args, **kwargs).get_position(2019)


def part2(*args, **kwargs):
    deck_size = 119315717514047
    # ss = SlamShuffle(*args, deck_size=119315717514047, **kwargs)
    ss = SlamShuffle(*args, **kwargs)
    ss.inp = reversed(ss.inp)
    pos2020 = 2020

    print_step = 0.01
    step2pos = {}
    for x in range(101741582076661):
        pos2020 = ss.reverse_shuffle(pos2020, deck_size)

        if pos2020 == 2020:
            raise ValueError()
        # step2pos[pos2020] = x

        if x > 101741582076661 * print_step:
            print(f'{x} from 101741582076661 ({100*x/101741582076661}% complete)')
            print_step += 0.01

    return pos2020


if __name__ == '__main__':
    for res in (
        # test1(),
        # part1(),
        part2(),
    ):
        print(res)
