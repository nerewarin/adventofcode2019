"""
--- Day 15: Oxygen System ---

https://adventofcode.com/2019/day/15

"""

import collections

from _intcode_computer import IntcodeComputer

TILE2DRAW = {
    0: '#',
    1: '.',
    2: '~',
    -1: ' ',
}


class PathFinder:
    def find_steps_to_oxygen(self, to_draw):
        # min_dist = float('inf')
        root = (0, 0)
        return self._bfs(root, to_draw)

    @staticmethod
    def _get_node(vertex, direction):
        # Only four movement commands are understood: north (1), south (2), west (3), and east (4)
        if direction == 1:
            up = (vertex[0], vertex[1] - 1)
            return up
        elif direction == 2:
            down = (vertex[0], vertex[1] + 1)
            return down
        elif direction == 3:
            left = (vertex[0] - 1, vertex[1])
            return left
        elif direction == 4:
            right = (vertex[0] + 1, vertex[1])
            return right
        raise RuntimeError('_get_node fcked up')

    def _bfs(self, root, to_draw):
        state = 1
        computer = IntcodeComputer()
        seen = {root: (state, computer)}
        queue = collections.deque(
            [(root, 0, computer)]
        )
        visit_order = []
        levels = []

        while queue:
            vertex, level, parent_computer = queue.popleft()
            visit_order.append(vertex)
            levels.append(level)

            if vertex in seen:
                _node = seen[vertex]
                _state = _node[0]
                if _state == 2:
                    if to_draw:
                        print(visit_order)
                        print(levels)
                    return level

            # for node in graph.get(vertex, [0, 1, 2, 3]):
            # Only four movement commands are understood: north (1), south (2), west (3), and east (4)
            if to_draw:
                print(f'before: vertex {vertex} pos {parent_computer.pos} base {parent_computer.relative_base}')
            for direction in range(1, 5):
                node = self._get_node(vertex, direction)
                if node in seen:
                    continue

                computer = parent_computer.copy()

                computer.feed(direction)
                try:
                    state = next(computer)
                    # 0: The repair droid hit a wall. Its position has not changed.
                    # 1: The repair droid has moved one step in the requested direction.
                    # 2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
                except StopIteration as e:
                    break

                # print('compare {node} to {vertex}:')
                # for i, val in enumerate(computer.memory):
                #     if val != seen[vertex][-1].memory[i]:
                #         print(i, val)
                # print('compare signals:')
                # print(computer.signals)
                # print(seen[vertex][-1].signals)

                if state == 0:
                    # 0: The repair droid hit a wall. Its position has not changed.
                    pass
                else:
                    queue.append(
                        (node, level + 1, computer)
                    )

                seen[node] = (state, computer)

                # draw region
                if to_draw:
                    ys = [pos[1] for pos in seen.keys()]
                    xs = [pos[0] for pos in seen.keys()]
                    min_y, max_y = min(ys), max(ys)
                    min_x, max_x = min(xs), max(xs)
                    print(f'after: node {node} state {state} pos {computer.pos} base {computer.relative_base}')
                    # print(f'after: vertex {vertex} pos {parent_computer.pos} base {parent_computer.relative_base}')
                    print('y from {} to {}'.format(min_y, max_y))
                    print('x from {} to {}'.format(min_x, max_x))
                    for _y in reversed(range(min_y, max_y + 1)):
                        line = []
                        for _x in range(min_x, max_x + 1):
                            if (_x, _y) == (0, 0):
                                _draw = '*'
                            if (_x, _y) == node:
                                _draw = 'Ж'
                            else:
                                _node = seen.get((_x, _y), (-1,))
                                _state = _node[0]
                                _draw = TILE2DRAW[_state]
                            line.append(_draw)
                        print(''.join(line))
                    # end draw region

        raise RuntimeError('couldnt find oxygen')


def part1(*args, **kwargs):
    return PathFinder().find_steps_to_oxygen(*args, **kwargs)


if __name__ == '__main__':
    for res in (
        part1(to_draw=False),
        # part1(to_draw=True),
    ):
        print(res)
