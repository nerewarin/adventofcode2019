for _y in range(y - 100, y):
    for _x in range(x - 100, x):
        computer = IntcodeComputer()
        computer.feed(_x)
        computer.feed(_y)
        value = next(computer)
        print(f'feed ({_x}, {_y}) => {value}')

        if value == 0:
            for _y in range(y - 100, y):
                for _x in range(x - 100, x):
                    computer = IntcodeComputer()
                    computer.feed(_x)
                    computer.feed(_y)
                    value = next(computer)
                    print(f'feed ({_x}, {_y}) => {value}')

                    if value == 0:
                        print(_x, _y)
                        raise RuntimeError('bad!')
            else:
                print(_x * 10000 + _y)
                # 6650385 is too low
                raise RuntimeError('ok!')

else:
    print(_x * 10000 + _y)
    # 6650385 is too low
    raise RuntimeError('ok!')

