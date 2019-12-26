import collections
from typing import Iterator

from _tools import get_puzzle_input


default_memory = get_puzzle_input()


class NoSignal(Exception):
    pass


class Memory(collections.defaultdict):
    def __init__(self):
        super().__init__(int)

    def __str__(self):
        return str({k: v for k, v in self})

    def copy(self):
        new = self.__class__()
        for k, v in self.items():
            new[k] = v
        return new


class IntcodeComputer(Iterator):
    def __init__(self, memory=None, signals=None, relative_base=None, pos=None, step=None):
        self.memory = self._init_memory(memory)
        self.signals = signals or []

        self.output = []

        self.gen = self._compute()

        self._pos = pos or 0
        self.relative_base = relative_base or 0
        self.step = step or 0

    def _init_memory(self, memory):
        if isinstance(memory, Memory):
            return memory

        if memory is None:
            memory = default_memory
        elif isinstance(memory, list):
            pass
        else:
            memory = [int(x) for x in memory.split(',')]

        mem = Memory()
        for i, val in enumerate(memory):
            mem[i] = val
        return mem

    def __next__(self):
        return next(self.gen)

    def feed(self, value):
        # feed the generator
        print(f'{value}', end=' ')
        self.signals.append(value)

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

    def _get_op3_input(self):
        if self.signals:
            return self.signals.pop(0)
        # return input('Enter instruction:\n')
        self.gen = self._compute()
        raise NoSignal()

    def _on_step_start(self):
        pass

    def compute(self):
        return list(self._compute())

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    def _compute(self):
        def _get_param(data, param, mode, base):
            if mode == 0:
                return data[param]
            elif mode == 1:
                return param
            elif mode == 2:
                return data[param + base]

        while True:
            self._on_step_start()

            instruction = self.memory[self.pos]
            instruction_str = f'{instruction:05d}'

            op_code = int(instruction_str[-2:])
            mode1 = int(instruction_str[-3])
            mode2 = int(instruction_str[-4])
            mode3 = int(instruction_str[-5])
            if mode3 == 2:
                pass

            if op_code == 1:
                op1, op2, op3 = self.memory[self.pos + 1], self.memory[self.pos + 2], self.memory[self.pos + 3]
                op1, op2 = _get_param(self.memory, op1, mode1, self.relative_base), _get_param(self.memory, op2, mode2, self.relative_base)
                if mode3 == 2:
                    op3 += self.relative_base

                self.memory[op3] = op1 + op2

                self.pos += 4
            elif op_code == 2:
                op1, op2, op3 = self.memory[self.pos + 1], self.memory[self.pos + 2], self.memory[self.pos + 3]
                op1, op2 = _get_param(self.memory, op1, mode1, self.relative_base), _get_param(self.memory, op2, mode2, self.relative_base)
                if mode3 == 2:
                    op3 += self.relative_base

                self.memory[op3] = op1 * op2

                self.pos += 4
            elif op_code == 3:
                op1 = self.memory[self.pos + 1]
                if mode1 == 2:
                    op1 += self.relative_base
                else:
                    pass

                self.memory[op1] = self._get_op3_input()

                self.pos += 2

            elif op_code == 4:
                op1 = self.memory[self.pos + 1]
                if mode1 == 2:
                    op1 += self.relative_base
                    op1 = self.memory[op1]
                else:
                    op1 = _get_param(self.memory, op1, mode1, self.relative_base)

                self.output.append(op1)
                self.step += 1
                self.pos += 2
                yield op1

            elif op_code == 5:
                op1 = self.memory[self.pos + 1]
                op1 = _get_param(self.memory, op1, mode1, self.relative_base)
                if op1 != 0:
                    op2 = self.memory[self.pos + 2]
                    op2 = _get_param(self.memory, op2, mode2, self.relative_base)
                    self.pos = op2
                else:
                    self.pos += 3

            elif op_code == 6:
                op1 = self.memory[self.pos + 1]
                op1 = _get_param(self.memory, op1, mode1, self.relative_base)
                if op1 == 0:
                    op2 = self.memory[self.pos + 2]
                    op2 = _get_param(self.memory, op2, mode2, self.relative_base)
                    self.pos = op2
                else:
                    self.pos += 3

            elif op_code == 7:
                op1, op2, op3 = self.memory[self.pos + 1], self.memory[self.pos + 2], self.memory[self.pos + 3]
                op1, op2 = _get_param(self.memory, op1, mode1, self.relative_base), _get_param(self.memory, op2, mode2, self.relative_base)

                if mode3 == 2:
                    op3 += self.relative_base

                self.memory[op3] = int(op1 < op2)

                self.pos += 4

            elif op_code == 8:
                op1, op2, op3 = self.memory[self.pos + 1], self.memory[self.pos + 2], self.memory[self.pos + 3]
                op1, op2 = _get_param(self.memory, op1, mode1, self.relative_base), _get_param(self.memory, op2, mode2, self.relative_base)

                if mode3 == 2:
                    op3 += self.relative_base

                self.memory[op3] = int(op1 == op2)

                self.pos += 4

            elif op_code == 9:
                op1 = self.memory[self.pos + 1]
                op1 = _get_param(self.memory, op1, mode1, self.relative_base)
                self.relative_base += op1

                self.pos += 2

            elif op_code == 99:
                break
            else:
                # error
                print(f'bad opp code: pos {self.pos} op_code {op_code}')
                raise ValueError(f'bad opp code: pos {self.pos} op_code {op_code}')

        return None

    def copy(self):
        # return self.__class__(memory=self.memory.copy(), signals=list(self.signals), gen=self.gen)
        return self.__class__(
            memory=self.memory.copy(),
            signals=list(self.signals),
            relative_base=self.relative_base,
            pos=self.pos,
            step=self.step,
        )
