from typing import Iterator
from _tools import get_puzzle_input


default_memory = get_puzzle_input()


class IntcodeComputer(Iterator):
    def __init__(self, memory=None, signals=None, gen_mode=False):
        if memory is None:
            memory = default_memory
        else:
            memory = [int(x) for x in memory.split(',')]

        self.signals = signals or []

        self.gen_mode = gen_mode
        self.gen = self._compute(gen_mode) if gen_mode else None
        self.memory = memory[:]
        self.memory.extend([0] * 1000)

        self.relative_base = 0

        self.output = []
        self._step = -1

    def __next__(self):
        return next(self.gen)

    def feed(self, value):
        # feed the generator
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
        return self.signals.pop(0)

    def _on_step_start(self):
        pass

    def compute(self):
        return list(self._compute())

    def _compute(self, gen_mode=False):
        def _get_param(data, param, mode, base):
            if mode == 0:
                return data[param]
            elif mode == 1:
                return param
            elif mode == 2:
                return data[param + base]

        data = self.memory

        relative_base = 0
        pos = 0

        while True:
            self._step += 1

            self._on_step_start()

            instruction = data[pos]
            instruction_str = f'{instruction:05d}'

            op_code = int(instruction_str[-2:])
            mode1 = int(instruction_str[-3])
            mode2 = int(instruction_str[-4])
            mode3 = int(instruction_str[-5])
            if mode3 == 2:
                pass

            if op_code == 1:
                op1, op2, op3 = data[pos + 1], data[pos + 2], data[pos + 3]
                op1, op2 = _get_param(data, op1, mode1, relative_base), _get_param(data, op2, mode2, relative_base)
                if mode3 == 2:
                    op3 += relative_base

                data[op3] = op1 + op2

                pos += 4
            elif op_code == 2:
                op1, op2, op3 = data[pos + 1], data[pos + 2], data[pos + 3]
                op1, op2 = _get_param(data, op1, mode1, relative_base), _get_param(data, op2, mode2, relative_base)
                if mode3 == 2:
                    op3 += relative_base

                data[op3] = op1 * op2

                pos += 4
            elif op_code == 3:
                op1 = data[pos + 1]
                if mode1 == 2:
                    op1 += relative_base
                else:
                    pass

                data[op1] = self._get_op3_input()

                pos += 2

            elif op_code == 4:
                op1 = data[pos + 1]
                if mode1 == 2:
                    op1 += relative_base
                    op1 = data[op1]
                else:
                    op1 = _get_param(data, op1, mode1, relative_base)

                self.output.append(op1)
                if gen_mode:
                    yield op1
                pos += 2

            elif op_code == 5:
                op1 = data[pos + 1]
                op1 = _get_param(data, op1, mode1, relative_base)
                if op1 != 0:
                    op2 = data[pos + 2]
                    op2 = _get_param(data, op2, mode2, relative_base)
                    pos = op2
                else:
                    pos += 3

            elif op_code == 6:
                op1 = data[pos + 1]
                op1 = _get_param(data, op1, mode1, relative_base)
                if op1 == 0:
                    op2 = data[pos + 2]
                    op2 = _get_param(data, op2, mode2, relative_base)
                    pos = op2
                else:
                    pos += 3

            elif op_code == 7:
                op1, op2, op3 = data[pos + 1], data[pos + 2], data[pos + 3]
                op1, op2 = _get_param(data, op1, mode1, relative_base), _get_param(data, op2, mode2, relative_base)

                if mode3 == 2:
                    op3 += relative_base

                data[op3] = int(op1 < op2)

                pos += 4

            elif op_code == 8:
                op1, op2, op3 = data[pos + 1], data[pos + 2], data[pos + 3]
                op1, op2 = _get_param(data, op1, mode1, relative_base), _get_param(data, op2, mode2, relative_base)

                if mode3 == 2:
                    op3 += relative_base

                data[op3] = int(op1 == op2)

                pos += 4

            elif op_code == 9:
                op1 = data[pos + 1]
                op1 = _get_param(data, op1, mode1, relative_base)
                relative_base += op1

                pos += 2

            elif op_code == 99:
                break
            else:
                # error
                print(f'bad opp code: pos {pos} op_code {op_code}')
                raise ValueError(f'bad opp code: pos {pos} op_code {op_code}')

        return None
