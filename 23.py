"""
--- Day 23: Category Six ---

https://adventofcode.com/2019/day/23

"""

import re

from _intcode_computer import IntcodeComputer


class LongIDLE(Exception):
    pass


class IntcodeComputer23(IntcodeComputer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._idle_cycles = 0

    def feed(self, value):
        super().feed(value)
        self._idle_cycles = 0

    def _get_op3_input(self):
        if self.signals:
            val = self.signals.pop(0)
            print(f'used {val}')
            self._idle_cycles = 0
            return val
        print('used default')
        self._idle_cycles += 1
        return -1

    def _on_step_start(self):
        if self._idle_cycles > 5:
            self.gen = self._compute()
            raise LongIDLE()


class CategorySix:
    _jump_size = 4
    _rexp = re.compile(r'(\w+)\s+(\w)\s(\w)')

    def __init__(self, *args, network_size=50, **kwargs):
        self.network_size = network_size
        self.network = [
            IntcodeComputer23(signals=[computer_num]) for computer_num in range(network_size)
        ]

    def get_first_packet_to(self, expected_address):
        address = None
        computer_num = 0
        while address != expected_address:
            # receive
            print(f'receive from {computer_num}:')
            computer = self.network[computer_num]
            try:
                address = next(computer)
            except LongIDLE:
                print('IDLE address', end='\n\n')
                computer_num = (computer_num + 1) % self.network_size
                continue
            except StopIteration:
                print('StopIteration address', end='\n\n')
                computer_num = (computer_num + 1) % self.network_size
                continue

            try:
                x = next(computer)
            except LongIDLE:
                print('IDLE x', end='\n\n')
                computer_num = (computer_num + 1) % self.network_size
                continue

            y = next(computer)
            print(f'{address} {x} {y}')

            if address == expected_address:
                return y

            # send
            next_computer = self.network[address]
            next_computer.feed(x)
            next_computer.feed(y)
            print(f'send to {address}: {x} {y}', end='\n\n')

            computer_num = address


def part1(*args, **kwargs):
    return CategorySix(*args, **kwargs).get_first_packet_to(255)


if __name__ == '__main__':
    for res in (
        part1(),
    ):
        print(res)
