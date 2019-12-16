"""
--- Day 6: Universal Orbit Map ---

https://adventofcode.com/2019/day/6

"""

import os
import math
import re
import itertools
import collections

from dataclasses import dataclass
from typing import Tuple

import networkx


class UniversalOrbitMap:
    _inp_rexp = re.compile(r'(\w+)\)(\w+)', re.MULTILINE)

    def __init__(self, inp=None, mode=None):
        self.mode = mode

        if inp is None:
            with open(os.path.join('inputs', '{}.txt'.format(__file__.split('/')[-1].split('.')[0]))) as f:
                inp = f.read()

        edges = [self._inp_rexp.match(line.strip()).groups() for line in inp.split('\n') if line.strip()]

        self.edges = edges

        self.graph = networkx.DiGraph()
        self.graph.add_edges_from(edges)

    @property
    def direct_orbits(self):
        return len(self.edges)

    def get_indirect_orbits(self):
        g = self.graph

        root2child = {}
        for node, nbrsdict in g.adjacency():
            root2child[node] = len(networkx.descendants(g, node)) - len(nbrsdict)

        return sum(root2child.values())

    def orbit_count_checksums(self):
        return sum(len(networkx.descendants(self.graph, node)) for node, nbrsdict in self.graph.adjacency())
        # return self.direct_orbits + self.get_indirect_orbits()


inp1 = """
    COM)B
    B)C
    C)D
    D)E
    E)F
    B)G
    G)H
    D)I
    E)J
    J)K
    K)L
"""


def test(test_num):
    if test_num == 1:
        res = UniversalOrbitMap(inp1).orbit_count_checksums()
        assert res == 42, 'test{} failed!: {}'.format(test_num, res)
    else:
        raise ValueError('test{} not implemented'.format(test_num))
    return 'test{} ok'.format(test_num)


def part1():
    return UniversalOrbitMap().orbit_count_checksums()


def part2():
    method = NotImplemented
    return UniversalOrbitMap(mode=2).method()


if __name__ == '__main__':
    for res in (
        # test(1),
        part1(),
        # test(2),
        # part2(),
    ):
        print(res)
