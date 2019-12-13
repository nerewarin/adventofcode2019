"""
--- Day 12: The N-Body Problem ---

https://adventofcode.com/2019/day/12

"""

import os
import math
import re
import itertools

from dataclasses import dataclass
from typing import Tuple


@dataclass()
class _Moon:
    x: int
    y: int
    z: int

    vx: int = 0
    vy: int = 0
    vz: int = 0

    @property
    def coords(self):
        return self.x, self.y, self.z

    @coords.setter
    def coords(self, xyz):
        self.x, self.y, self.z = xyz

    @property
    def velocity(self):
        return self.vx, self.vy, self.vz

    @velocity.setter
    def velocity(self, xyz):
        self.vx, self.vy, self.vz = xyz

    def __repr__(self):
        return f'pos=<x={self.x}, y={self.y}, z={self.z}>, vel=<x={self.vx}, y={self.vy}, z={self.vz}>'

    @staticmethod
    def _get_velocity(a, b):
        if a > b:
            return -1
        elif a < b:
            return 1
        return 0

    @property
    def potential_energy(self):
        return sum(abs(coord) for coord in self.coords)

    @property
    def kinetic_energy(self):
        return sum(abs(coord) for coord in self.velocity)

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy

    def __str__(self):
        return f'pot: {self.potential_energy};   kin: {self.kinetic_energy};   total:  {self.total_energy}'


@dataclass
class Moon(_Moon):
    def update_velocity(self, moon: _Moon):
        self.vx += self._get_velocity(self.x, moon.x)
        self.vy += self._get_velocity(self.y, moon.y)
        self.vz += self._get_velocity(self.z, moon.z)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz


class NbodyProblem:
    inp_rexp = re.compile(r'<x=(-*\d+), y=(-*\d+), z=(-*\d+)>\s*')
    dim = 3

    def __init__(self, moons=None):
        if moons is None:
            with open(os.path.join('inputs', '{}.txt'.format(__file__.split('/')[-1].split('.')[0]))) as f:
                lines = f.readlines()
        else:
            lines = [line for line in moons.split('\n') if line.strip()]

        moons = [map(int, self.inp_rexp.match(moon).groups()) for moon in lines]

        self.moons = [Moon(*coords) for coords in moons]
        self.tick = 0
        self.history = [
            [] for x in range(self.dim)
        ]
        for idx in range(self.dim):
            coord_history = tuple(moon.coords[idx] for moon in self.moons)
            self.history[idx].append(coord_history)

        self.periods = [
            0 for x in range(self.dim)
        ]

    @property
    def period_found(self):
        return all(self.periods)

    def _update_history(self):
        for idx in range(self.dim):
            # if self.periods[idx]:
            #     continue

            coord_history = tuple(moon.coords[idx] for moon in self.moons)

            # if coord_history in self.history[idx] and self.tick - self.history[idx].index(coord_history) > 1:
            if coord_history in self.history[idx]:
                self.periods[idx] = self.tick

            self.history[idx].append(coord_history)

    @property
    def total_energy(self):
        return sum(moon.total_energy for moon in self.moons)

    def simulate(self, steps):
        for x in range(steps):
            self.tick += 1
            # print(f'After {x} steps:')
            # for moon in self.moons:
            #     print(moon)

            i = 0
            for moon1, moon2 in itertools.permutations(self.moons, 2):
                moon1.update_velocity(moon2)

                i += 1
                # print(i)
                # print(moon1)

            for moon in self.moons:
                moon.move()

            self._update_history()

        # print(f'After {x+1} steps:')
        # for moon in self.moons:
        #     print(repr(moon))

        # print('Energy after 10 steps:')
        # for moon in self.moons:
        #     print(str(moon))

        # print(self.total_energy)

    def find_period(self):
        self.simulate(2772)
        # while not self.period_found:
        #     self.simulate(1)

        return self.periods


inp = '''
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
'''


def test(test_num):
    if test_num == 1:
        res = NbodyProblem(inp).simulate(10)
        # assert res == 2772, 'test{} failed!: {}'.format(test_num, res)
    if test_num == 2:
        res = NbodyProblem(inp).find_period()
        assert res == 2772, 'test{} failed!: {}'.format(test_num, res)
    return 'test{} ok'.format(test_num)


def part1(*args, **kwargs):
    pr = NbodyProblem(*args)
    pr.simulate(1000)
    return pr.total_energy


def part2(*args, **kwargs):
    x, y = MonitoringStation(*args).vaporize(200)
    return x * 100 + y


if __name__ == '__main__':
    for res in (
        # test(1),
        # part1(),
        test(2),
        # part2(),
    ):
        print(res)
