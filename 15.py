"""
--- Day 15: Oxygen System ---

https://adventofcode.com/2019/day/15

"""

import os
import collections


class intcodeComputer:
    def __init__(self, memory=None, signals=None):
        if memory is None:
            with open(os.path.join('inputs', '{}.txt'.format(__file__.split('/')[-1].split('.')[0]))) as f:
                memory = f.read()
        # self.memory = Memory([int(x) for x in memory.split(',')])
        memory = [int(x) for x in memory.split(',')]

        self.signals = signals or []

        self.memory = collections.defaultdict(int)
        self.memory.update({
            idx: value for idx, value in enumerate(memory)
        })
        self.relative_base = 0
        self.gen = self.compute(gen_mode=True)

    def __next__(self):
        return next(self.gen)

    def get_value(self, val_or_idx, mode):
        if mode == 0:
            idx = val_or_idx
            if idx < 0:
                raise ValueError("idx {} cannot be negative!".format(mode))
            return self.memory[idx]
        elif mode == 1:
            val = val_or_idx
            return val
        elif mode == 2:
            idx = self.relative_base + val_or_idx
            if idx < 0:
                raise ValueError("idx {} cannot be negative!".format(mode))
            return self.memory[idx]
        else:
            raise ValueError("mode {} is unknown".format(mode))

    def get_write_idx(self, param, mode):
        if mode == 0:
            return param
        elif mode == 1:
            raise ValueError("mode {} is wrong for write mode!".format(mode))
        elif mode == 2:
            return param + self.relative_base
        else:
            raise ValueError("mode {} is unknown".format(mode))

    def compute(self, gen_mode=False):
        curr_idx = 0
        while True:
            instruction = self.memory[curr_idx]

            op = instruction % 100

            _ins = instruction // 100
            mode1 = _ins % 10

            _ins = _ins // 10
            mode2 = _ins % 10

            _ins = _ins // 10
            mode3 = _ins % 10

            if op == 99:
                return self.memory[0]

            param1 = self.memory[curr_idx + 1]
            param2 = self.memory[curr_idx + 2]
            try:
                param3 = self.memory[curr_idx + 3]
            except KeyError:
                param3 = None  # dirty but who cares

            if op < 3:
                shift = 4
                idx = self.get_write_idx(param3, mode3)
                if op == 1:
                    self.memory[idx] = self.get_value(param1, mode1) + self.get_value(param2, mode2)
                elif op == 2:
                    self.memory[idx] = self.get_value(param1, mode1) * self.get_value(param2, mode2)
            elif op < 5:
                shift = 2
                if op == 3:
                    # Opcode 3 takes a single integer as input and saves it to the position given by its only parameter
                    # idx = self.relative_base + param1
                    # idx = self.get_value(param1, mode1)
                    # idx = param1
                    idx = self.get_write_idx(param3, mode3)
                    if self.signals:
                        signal = self.signals.pop(0)
                    else:
                        signal = int(input('input:'))
                    self.memory[idx] = signal
                elif op == 4:
                    out = self.get_value(param1, mode1)
                    if out not in range(3):
                        # The repair droid can reply with any of the following status codes:
                        # 0: The repair droid hit a wall. Its position has not changed.
                        # 1: The repair droid has moved one step in the requested direction.
                        # 2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
                        raise ValueError('wrong output {}'.format(out))
                    if gen_mode:
                        yield out
                    else:
                        return out
            elif op < 7:
                # jump-if-true
                if op == 5 and self.get_value(param1, mode1):
                    shift = self.get_value(param2, mode2) - curr_idx
                # jump-if-false
                elif op == 6 and not self.get_value(param1, mode1):
                    shift = self.get_value(param2, mode2) - curr_idx
                else:
                    shift = 3
            elif op < 9:
                # less than
                if op == 7 and self.get_value(param1, mode1) < self.get_value(param2, mode2):
                    _val = 1
                # equals
                elif op == 8 and self.get_value(param1, mode1) == self.get_value(param2, mode2):
                    _val = 1
                else:
                    _val = 0
                idx = self.get_write_idx(param3, mode3)
                self.memory[idx] = _val
                shift = 4
            elif op == 9:
                # Opcode 9 adjusts the relative base by the value of its only parameter
                self.relative_base += self.get_value(param1, mode1)
                shift = 2
            else:
                raise NotImplemented("op={} is unknown".format(op))

            curr_idx += shift

    def find_steps_to_oxygen(self):
        # min_dist = float('inf')
        root = (0, 0)
        return self._bfs(root) - 1

    def feed(self, value):
        # feed the generator
        self.signals.append(value)

    def _get_node(self, vertex, direction):
        # Only four movement commands are understood: north (1), south (2), west (3), and east (4)
        if direction == 1:
            up = (vertex[0], vertex[1] + 1)
            return up
        elif direction == 2:
            down = (vertex[0], vertex[1] - 1)
            return down
        elif direction == 3:
            left = (vertex[0] - 1, vertex[1])
            return left
        elif direction == 4:
            right = (vertex[0] + 1, vertex[1])
            return right
        raise RuntimeError('_get_node fcked up')

    def _bfs(self, root):
        state = 1
        seen, queue = {root: state}, collections.deque([(root, 0)])
        visit_order = []
        levels = []

        while state != 2:
            vertex, level = queue.popleft()
            visit_order.append(vertex)
            levels.append(level)

            # for node in graph.get(vertex, [0, 1, 2, 3]):
            for direction in range(1, 5):
                node = self._get_node(vertex, direction)
                if node not in seen:
                    self.feed(direction)

                    try:
                        state = next(self)
                    except StopIteration as e:
                        # last_system_outputs.append(last_system_output)
                        break

                    if state != 0:
                        # 0: The repair droid hit a wall. Its position has not changed.
                        queue.append((node, level + 1))

                    # seen[node] = (computer, state)
                    seen[node] = state

        print(visit_order)
        print(levels)
        return levels


def part1(*args, **kwargs):
    return intcodeComputer(*args, **kwargs).find_steps_to_oxygen()


def part2(*args, **kwargs):
    return intcodeComputer(*args, signals=[2], **kwargs).compute()


inp = '''
      
      
   D  
      
      
'''


def test(test_num, mode=0):
    if test_num == 1:
        res = intcodeComputer(inp).compute()
        assert res == 31, 'test{} failed!: {}'.format(test_num, res)
    if test_num == 2:
        res = intcodeComputer(inp2).get_ore_for_fuel()
        assert res == 165, 'test{} failed!: {}'.format(test_num, res)
    if test_num == 3:
        _inp = inp3
        if not mode:
            res = intcodeComputer(_inp).get_ore_for_fuel()
            assert res == 13312, 'test{} failed!: {}'.format(test_num, res)
        else:
            res = get_fuel_for_ore(ore_mode_2, _inp)
            assert res == 82892753, 'test{} failed!: {}'.format(test_num, res)

    if test_num == 4:
        _inp = inp4
        if not mode:
            res = intcodeComputer(inp4).get_ore_for_fuel()
            assert res == 180697, 'test{} failed!: {}'.format(test_num, res)
        else:
            res = get_fuel_for_ore(ore_mode_2, _inp)
            assert res == 5586022 , 'test{} failed!: {}'.format(test_num, res)

    if test_num == 5:
        _inp = inp5
        if not mode:
            res = intcodeComputer(_inp).get_ore_for_fuel()
            assert res == 2210736, 'test{} failed!: {}'.format(test_num, res)
        else:
            res = get_fuel_for_ore(ore_mode_2, _inp)
            assert res == 460664, 'test{} failed!: {}'.format(test_num, res)

    return 'test{} ok'.format(test_num)


def part1(*args, **kwargs):
    computer = intcodeComputer(*args, **kwargs)
    return computer.find_steps_to_oxygen()

#
# def part2(*args, **kwargs):
#     return get_fuel_for_ore()


if __name__ == '__main__':
    for res in (
        # test(1),
        # test(2),
        # test(3),
        # test(4),
        # test(5),
        part1(),
        # test(3, mode=2),
        # test(4, mode=2),
        # test(5, mode=2),
        # part2(),
    ):
        print(res)
