import collections


def get_input():
    with open('inputs/11.txt', 'r') as f:
        return (int(i) for i in f.readline().split(','))


def _get_param(data, param, mode, base):
    if mode == 0:
        return data[param]
    elif mode == 1:
        return param
    elif mode == 2:
        return data[param + base]


def run(code):
    data = code[:]
    data.extend([0] * 1000)

    robot_pos = (0, 0)
    # up, left, down, right
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    direction = 0
    colors = collections.defaultdict(list)

    input_ = []
    output = []

    relative_base = 0
    pos = 0

    input_.append(1)

    print('start input 0')
    while True:
        # print(data)
        if len(output) == 2:
            # paint
            colors[robot_pos].append(output.pop(0))
            turn = output.pop(0)
            if turn == 0:
                # turn left
                direction = (direction + 1) % 4
            elif turn == 1:
                # turn right
                direction = (direction - 1) % 4

            print('on position {} got paint {} turn {}'.format(robot_pos, colors[robot_pos][-1], turn))

            robot_pos = (robot_pos[0] + directions[direction][0], robot_pos[1] + directions[direction][1])
            print('move to ', robot_pos)
            # calc input
            if robot_pos in colors:
                print('input ', colors[robot_pos][-1])
                input_.append(colors[robot_pos][-1])
            else:
                print('input default (0)')
                input_.append(0)
            print()

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
                # op1 = _get_param(data, op1, mode1, relative_base)
            data[op1] = input_.pop()

            pos += 2

        elif op_code == 4:
            op1 = data[pos + 1]
            if mode1 == 2:
                op1 += relative_base
                op1 = data[op1]
            else:
                op1 = _get_param(data, op1, mode1, relative_base)

            output.append(op1)
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

    return colors


def solve(data):
    data = list(data)
    output = run(data)
    print(len(output))

    print('output')
    for n, (i, color) in enumerate(output.items()):
        print(i, color)

    min_y = min(i[1] for i in output)
    max_y = max(i[1] for i in output)
    min_x = min(i[0] for i in output)
    max_x = max(i[0] for i in output)

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x + 1):
            if (x, y) in output:
                color = output[(x, y)][-1]
            else:
                color = -1

            print(('_', '#', '.')[color], end='')
        print()

    print(len(output))
    return None


def main():
    data = get_input()
    print(solve(data))


if __name__ == '__main__':
    main()

# 87571
