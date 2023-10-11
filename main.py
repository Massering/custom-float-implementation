import sys
from fixed_point import FixedPoint
from single_point import Single
from half_point import Half


if __name__ == '__main__':
    FORMAT, rounding_type, *args = map(str, sys.argv[1:])

    if rounding_type != '1':
        print('Wrong rounding type')
        exit(0)

    if '.' in FORMAT:
        FixedPoint.A, FixedPoint.B = tuple(map(int, FORMAT.split('.')))
        if len(args) == 1:
            a = FixedPoint(args[0])
            print(a)
        else:
            a, act, b = args
            a = FixedPoint(a)
            # print('a:', a, [a])
            b = FixedPoint(b)
            # print('b:', b, [b])
            if int(b) == 0 and act == '/':
                print('error')
                exit(0)
            c = eval(f'a {act} b')
            print(c)

    elif FORMAT == 'f':
        if len(args) == 1:
            a = Single(args[0])
            print(a)
        else:
            a, act, b = args
            a = Single(a)
            b = Single(b)
            c = eval(f'a {act} b')
            print(c)
            # print([c])

    elif FORMAT == 'h':
        if len(args) == 1:
            a = Half(args[0])
            print(a)
        else:
            a, act, b = args
            a = Half(a)
            b = Half(b)
            c = eval(f'a {act} b')
            print(c)
            # print([c])

    else:
        print('Wrong format')

'''
16.12 1 0x17360
8.8 1 0xdc9f + 0xd736
8.8 1 0x300 * 0x500
f 1 0xB9CD542
f 1 0x414587dd * 0x42ebf110
h 1 0x4145 * 0x42eb
f 1 0x1 / 0x0

'''
