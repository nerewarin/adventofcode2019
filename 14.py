"""
--- Day 14: Space Stoichiometry ---

https://adventofcode.com/2019/day/14

"""

import os
import collections
import math
import re
import itertools

from dataclasses import dataclass
from typing import Tuple


class SpaceStoichiometry:
    _reaction_rexp = re.compile(r'(\d+)\s(\w+)')
    _consumed_ore_key = 'consumed ORE'

    def __init__(self, inp=None):
        if inp is None:
            with open(os.path.join('inputs', '{}.txt'.format(__file__.split('/')[-1].split('.')[0]))) as f:
                lines = f.readlines()
        else:
            lines = [line for line in inp.split('\n') if line.strip()]

        self.expressions = {}
        for line in lines:
            *consumes, produce = self._reaction_rexp.findall(line)
            self.expressions[produce[1]] = {
                'count': int(produce[0]),
                'ingredients': {
                    consume[1]: int(consume[0]) for consume in consumes
                }
            }

        self.costs = {}
        self._indent = ''

    def _cook(self, required_ingredient, required_amount, bag, indent=None):
        """Minimum amount of ORE required to produce exactly 1 <ingredient>

        Returns:
            int: amount of ORE needed to produce one <ingredient>

        """
        if indent is None:
            indent = self._indent
        formula = self.expressions[required_ingredient]
        print('{}cooking {} {} by formula {}, bag={}'.format(indent, required_amount, required_ingredient, formula, bag))
        self._indent += ' '

        # if required_ingredient in self.costs:
        #     # cache
        #     return self.costs[required_ingredient]

        ing_key = 'ingredients'
        result_amount_key = 'count'
        ore_key = 'ORE'

        unused_ing_amount = bag[required_ingredient]
        if unused_ing_amount:
            _required_amount = required_amount - unused_ing_amount
            if _required_amount < 0:
                bag[required_ingredient] -= required_amount
                return bag

            bag[required_ingredient] -= unused_ing_amount
            required_amount = _required_amount

        formula_output_amount = formula[result_amount_key]
        required_operations = math.ceil(required_amount / formula_output_amount)
        _consumed_ore_by_formula = 0
        for ing_name, ing_amount in formula[ing_key].items():
            if ing_name == ore_key:
                _consumed_ore_value = required_operations * ing_amount

                unused_ing_amount = required_operations * formula_output_amount - required_amount
                if unused_ing_amount < 0:
                   raise RuntimeError('fix me')

                bag[required_ingredient] += unused_ing_amount
                bag[self._consumed_ore_key] += _consumed_ore_value

                _consumed_ore_by_formula += _consumed_ore_value
            else:
                _consumed_ore_before = bag[ore_key]

                # assert res == 180697
                _to_cook = ing_amount * required_operations  # test4 failed!: 182966
                # _to_cook = math.ceil(ing_amount * (required_amount / formula_output_amount))  # test4 failed!: 179537

                self._cook(ing_name, _to_cook, bag, indent + ' ')
                _consumed_ore_by_formula += bag[ore_key] - _consumed_ore_before

        print('{}cooked {} {} by formula {}, consumed={}, bag={}'.format(indent, required_amount, required_ingredient, formula, _consumed_ore_by_formula, bag))
        return bag

    def get_fuel_cost(self):
        """Minimum amount of ORE required to produce exactly 1 FUEL

        Returns:
            int: amount of ORE needed to produce one FUEL

        """
        bag = Bag()
        self._cook('FUEL', 1, bag)
        return bag[self._consumed_ore_key]


class Bag(collections.defaultdict):
    def __init__(self):
        super().__init__(int)

    def __str__(self):
        return str({k: v for k, v in self.items() if v})


inp = '''
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
'''

inp2 = '''
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
'''


inp3 = '''
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
'''

inp4 = '''
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
'''

inp5 = '''
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
'''


def test(test_num):
    if test_num == 1:
        res = SpaceStoichiometry(inp).get_fuel_cost()
        assert res == 31, 'test{} failed!: {}'.format(test_num, res)
    if test_num == 2:
        res = SpaceStoichiometry(inp2).get_fuel_cost()
        assert res == 165, 'test{} failed!: {}'.format(test_num, res)
    if test_num == 3:
        res = SpaceStoichiometry(inp3).get_fuel_cost()
        assert res == 13312, 'test{} failed!: {}'.format(test_num, res)
    if test_num == 4:
        res = SpaceStoichiometry(inp4).get_fuel_cost()
        assert res == 180697, 'test{} failed!: {}'.format(test_num, res)
    if test_num == 5:
        res = SpaceStoichiometry(inp5).get_fuel_cost()
        assert res == 2210736, 'test{} failed!: {}'.format(test_num, res)
    return 'test{} ok'.format(test_num)


def part1(*args, **kwargs):
    return SpaceStoichiometry(*args).get_fuel_cost()


def part2(*args, **kwargs):
    x, y = MonitoringStation(*args).vaporize(200)
    return x * 100 + y


if __name__ == '__main__':
    for res in (
        # test(1),
        # test(2),
        # test(3),
        test(4),
        # test(5),
        # part1(),
        # part2(),
    ):
        print(res)
