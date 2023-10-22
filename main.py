import sys
from fixed_point import FixedPoint
from single_point import Single
from half_point import Half


if __name__ == '__main__':
    try:
        FORMAT, rounding_type, *args = map(str, sys.argv[1:])
        assert len(args) == 1 or len(args) == 3
    except Exception:
        print("Wrong number of input arguments", file=sys.stderr)
        exit(777)

    if rounding_type != '1':
        print('Wrong rounding type', file=sys.stderr)
        exit(777)

    if '.' in FORMAT:
        FixedPoint.A, FixedPoint.B = tuple(map(int, FORMAT.split('.')))
        if len(args) == 1:
            a = FixedPoint(args[0])
            print(str(a))
        else:
            a, act, b = args
            a = FixedPoint(a)
            b = FixedPoint(b)
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

    else:
        print('Wrong format of input data', file=sys.stderr)
        exit(777)
