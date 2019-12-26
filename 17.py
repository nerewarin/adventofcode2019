"""
--- Day 17: Set and Forget ---

https://adventofcode.com/2019/day/17

"""

from _intcode_computer import IntcodeComputer, NoSignal


class SetAndForget(IntcodeComputer):
    def __init__(self, _map=None, memory_changes=None):
        self._memory_changes = memory_changes or {}

        super().__init__()

        if _map:
            self._map = '\n'.join(_map)
        else:
            self._map = self._get_msg()

    def _get_msg(self):
        chars = []
        while True:
            try:
                ascii_code = chr(next(self))
                chars.append(ascii_code)
            except NoSignal:
                break
            except StopIteration:
                break
        return ''.join(chars)

    def _init_memory(self, memory):
        _memory = super()._init_memory(memory)
        for k, v in self._memory_changes.items():
            _memory[k] = v
        return _memory

    def _draw(self):
        for symbol in self._map:
            if symbol in '^v<>X':
                vacuum_robot_xy = symbol
            print(symbol, end='')
        # print(f'\nvacuum_robot_xy: {vacuum_robot_xy}')

    @staticmethod
    def _get_value(layout, x, y):
        if y < 0 or y >= len(layout):
            return 0
        row = layout[y]
        if x < 0 or x >= len(row):
            return 0
        return row[x] == '#'

    def all_adjacent_are_scaffold(self, layout, x, y):
        return all((
            self._get_value(layout, x + 1, y),
            self._get_value(layout, x - 1, y),
            self._get_value(layout, x, y + 1),
            self._get_value(layout, x, y - 1),
        ))

    def get_sum_of_the_alignment_parameters(self):
        self._draw()

        layout = self._map.split('\n')
        alignments = []
        res = 0
        for y, row in enumerate(layout):
            for x, symbol in enumerate(row):
                if symbol == '#' and self.all_adjacent_are_scaffold(layout, x, y):
                    alignments.append((x, y))
                    res += x * y
        return res

    def collect_dust(self):
        self._draw()

        commands = self._get_commands()

        self._input_commands(commands)

        # video_enabled = 'y'
        video_disabled = 'n'
        self.feed(ord(video_disabled))
        self.feed(self._new_line)

        msg = self._get_msg()
        # print()
        # print(msg)
        return ord(msg[-1])

    def _get_commands(self):
        robot_pos = self._map.index('^')
        L = 'L'
        R = 'R'
        a = 12
        b = 10
        c = 8
        A = L, a, L, b, R, c, L, a,
        B = R, c, R, b, R, a
        C = L, b, R, a, R, c,
        return {
            'A': A,
            'B': B,
            'C': C,
            'path': 'ABABCCBABC',
        }

    @property
    def _new_line(self):
        return 10  # ord('\n')

    @property
    def _comma(self):
        return 44  # ord('\,')

    def _input_commands(self, commands):
        command_path = commands['path']
        for i, x in enumerate(command_path[:-1]):
            self.feed(ord(x))
            self.feed(self._comma)
        self.feed(ord(command_path[-1]))
        self.feed(self._new_line)

        print(self._get_msg())

        for command_description in ('A', 'B', 'C'):
            command = commands[command_description]
            for x in command[:-1]:
                for val in str(x):
                    self.feed(ord(val))
                self.feed(self._comma)

            for val in str(command[-1]):
                self.feed(ord(val))
            self.feed(self._new_line)

            msg = self._get_msg()
            print()
            print(msg)


def part1(*args, **kwargs):
    return SetAndForget(*args, **kwargs).get_sum_of_the_alignment_parameters()


def part2(*args, **kwargs):
    return SetAndForget(*args, **kwargs).collect_dust()


def test(test_num):
    _inp = '''
        ..#..........
        ..#..........
        #######...###
        #.#...#...#.#
        #############
        ..#...#...#..
        ..#####...^..
    '''
    test_inp = [val.strip() for val in _inp.split('\n') if val.strip()]
    if test_num == 1:
        res = SetAndForget(test_inp).get_sum_of_the_alignment_parameters()
        assert res == 76, 'test{} failed!: {}'.format(test_num, res)
    else:
        raise NotImplementedError(f'unknown test_num = {test_num}')

    return 'test{} ok'.format(test_num)


if __name__ == '__main__':
    for res in (
        # test(1),
        # part1(),
        part2(memory_changes={0: 2}),
    ):
        print(res)
