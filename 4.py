"""
--- Day 4: Secure Container ---

https://adventofcode.com/2019/day/4

"""

import os
import math
import re
import itertools
import collections

from dataclasses import dataclass
from typing import Tuple


class SecureContainer:
    def __init__(self, inp=None, mode=None):
        if inp is None:
            with open(os.path.join('inputs', '{}.txt'.format(__file__.split('/')[-1].split('.')[0]))) as f:
                inp = f.read()

        self.min, self.max = (int(digit) for digit in inp.split('-'))

    def count_different_passwords(self):
        """
        How many different passwords within the range given in your puzzle input meet these criteria?

        - It is a six-digit number.
        - The value is within the range given in your puzzle input.
        - Two adjacent digits are the same (like 22 in 122345).
        - Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

        Returns:
            int

        """
        res = 0
        for candidate in range(self.min, self.max):
            # Two adjacent digits are the same (like 22 in 122345).
            # counter = collections.Counter()
            candidate_str = str(candidate)
            has_adjacent = False
            decreases = False
            for idx in range(len(candidate_str) - 1):
                first = candidate_str[idx]
                second = candidate_str[idx + 1]
                if first == second:
                    has_adjacent = True

                # Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
                if int(second) < int(first):
                    decreases = True
                    break

            if not has_adjacent:
                continue

            if decreases:
                continue

            res += 1
            # print('{}. {}'.format(res, candidate))

        # 204503 is too high
        # 1246 wrong account? lol
        return res


inp = '245318-765747'


def part1():
    return SecureContainer(inp).count_different_passwords()


if __name__ == '__main__':
    for res in (
        part1(),
    ):
        print(res)
