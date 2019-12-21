"""
--- Day 21: Springdroid Adventure ---

https://adventofcode.com/2019/day/21

"""

import collections

from _intcode_computer import IntcodeComputer

TILE2DRAW = {
    0: '#',
    1: '.',
    2: '~',
    -1: ' ',
}


class NoSignal(Exception):
    pass


class IntcodeComputer21(IntcodeComputer):
    def _get_op3_input(self):
        if self.signals:
            return self.signals.pop(0)
        # return input('Enter instruction:\n')
        self.gen = self._compute()
        raise NoSignal()


class SpringScript:
    def __init__(self, to_draw=False):
        self.to_draw = to_draw
        # Two registers are available: T, the temporary value register, and J, the jump register

        # Your springdroid can detect ground at four distances:
        # one tile away (A), two tiles away (B), three tiles away (C), and four tiles away (D).
        # If there is ground at the given distance, the register will be true; if there is a hole,
        # the register will be false
        self.registers = {
            'T': False,  # temporary value register
            'J': False,  # jump register
            'A': False,  # is there ground 1 tile away
            'B': False,  # is there ground 2 tiles away
            'C': False,  # is there ground 3 tiles away
            'D': False,  # is there ground 4 tiles away
        }

        self.computer = IntcodeComputer21()

    @staticmethod
    def _check_is_writable(y):
        return y in ('T', 'J')

    def _and(self, x, y):
        self._check_is_writable(y)

        val = self.registers[x] and self.registers[y]
        self.registers[y] = val
        return val

    def _or(self, x, y):
        self._check_is_writable(y)

        val = self.registers[x] or self.registers[y]
        self.registers[y] = val
        return val

    def _not(self, x, y):
        self._check_is_writable(y)

        val = not self.registers[x]
        self.registers[y] = val
        return val

    @staticmethod
    def _get_string_in_ascii(s):
        return [ord(c) for c in s] + [10]

    def _get_walk_program(self):
        """
        There are only three instructions available in springscript:

        AND X Y sets Y to true if both X and Y are true; otherwise, it sets Y to false.
        OR X Y sets Y to true if at least one of X or Y is true; otherwise, it sets Y to false.
        NOT X Y sets Y to true if X is false; otherwise, it sets Y to false.

        Returns:
            list of int: ASCII code

        """

    def get_amout_of_hull_damage(self):
        # while self.computer.signals:
        try:
            for out in self.computer.gen:
                # print(f'{chr(out)} ({out})', end='')
                print(f'{chr(out)}', end='')
        except NoSignal:
            # # now enter the program
            # for instruction_code in self._get_walk_program():
            #     self.computer.feed(instruction_code)

            walk = self._get_string_in_ascii('WALK')
            for instruction_code in walk:
                self.computer.feed(instruction_code)

        try:
            for out in self.computer.gen:
                print(f'{chr(out)}', end='')
        except NoSignal:
            a = 9


def part1(*args, **kwargs):
    return SpringScript(*args, **kwargs).get_amout_of_hull_damage()


if __name__ == '__main__':
    for res in (
        part1(),
    ):
        print(res)
