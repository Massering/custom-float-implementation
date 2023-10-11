import unittest
from main import *
from random import *


def gen_fixed_float(a, b) -> (FixedPoint, float):
    int_x = randint(0, 2 ** (a + b) - 1)
    # print(hex(int_x))

    bin_num = bin(int_x)[2:].zfill(a + b)
    n = 0
    base = 5
    for i in bin_num[len(bin_num) - b:]:
        n = (n + int(i) * base) * 10
        base *= 5

    base = 10 ** (b + 1)
    for i in bin_num[1:len(bin_num) - b][::-1]:
        n += int(i) * base
        base <<= 1
    n -= int(bin_num[0]) * base

    sign = '-' * (n != abs(n))
    n = str(abs(n)).zfill(b + 1)
    py_x = round(float(sign + n[:len(n) - b - 1] + '.' + n[len(n) - b - 1:]), 3)
    my_x = FixedPoint(hex(int_x))

    return hex(int_x), my_x, py_x


def gen_single_float() -> (Single, float):
    sign = randint(0, 1)
    exp = randint(1, 254)
    man = randint(0, 2 ** 23 - 1)
    py_x = int('-' * sign + '1') * (man + 2 ** 23) * 2 ** (exp - 127)
    h = hex(int(f'{sign}{bin(exp)[2:].zfill(8)}{bin(man)[2:].zfill(23)}', 2))
    my_x = Single(h)
    return h, my_x, py_x


def gen_half_float() -> (Half, float):
    sign = randint(0, 1)
    exp = randint(1, 30)
    man = randint(0, 2 ** 10 - 1)
    py_x = int('-' * sign + '1') * (man + 2 ** 10) * 2 ** (exp - 14)
    h = hex(int(f'{sign}{bin(exp)[2:].zfill(5)}{bin(man)[2:].zfill(10)}', 2))
    my_x = Half(h)
    return h, my_x, py_x


class MyTestCase(unittest.TestCase):
    def test_fixed(self):
        print('test_fixed')
        for i in range(100):
            length = randint(1, 32)
            a = randint(1, length)
            b = length - a
            FixedPoint.A, FixedPoint.B = a, b

            hex_x, my_x, py_x = gen_fixed_float(a, b)
            print(f'{i}. py main.py {a}.{b} 1 {hex_x}')
            self.assertEqual(f'{py_x:.3f}', str(my_x))

    def test_fixed_ops(self):
        print('test_fixed_ops')
        for i in range(100):
            length = randint(1, 32)
            a = randint(1, length)
            b = length - a
            FixedPoint.A, FixedPoint.B = a, b

            hex_x, my_x, py_x = gen_fixed_float(a, b)
            hex_y, my_y, py_y = gen_fixed_float(a, b)

            for act in '+-*/':
                print(f'{i}. py main.py {a}.{b} 1 {hex_x} {act} {hex_y}')
                if act == '/' and py_y == 0:
                    py_z = 'error'
                else:
                    py_z = f'{round(eval(f"py_x {act} py_y"), 3):.3f}'
                print('py:', py_x, act, py_y, '=', py_z)
                my_z = eval(f'my_x {act} my_y')
                print('my:', my_x, act, my_y, '=', my_z)
                print()
                self.assertEqual(0, 0)

    def test_single(self):
        print('test_single')
        for i in range(100):
            hex_x, my_x, py_x = gen_single_float()
            print(f'{i}. py main.py f 1 {hex_x}')
            print(my_x)
            self.assertEqual(0, 0)

    def test_single_ops(self):
        print('test_single_ops')
        for i in range(100):
            hex_x, my_x, py_x = gen_single_float()
            hex_y, my_y, py_y = gen_single_float()

            for act in '+-*/':
                print(f'{i}. py main.py f 1 {hex_x} {act} {hex_y}')
                if act == '/' and py_y == 0:
                    py_z = '+-inf'
                else:
                    py_z = f'{round(eval(f"py_x {act} py_y"), 3):.3f}'
                print('py:', py_x, act, py_y, '=', py_z)
                my_z = eval(f'my_x {act} my_y')
                print('my:', my_x, act, my_y, '=', my_z)
                print()
                self.assertEqual(0, 0)

    def test_half(self):
        print('test_half')
        for i in range(100):
            hex_x, my_x, py_x = gen_half_float()
            print(f'{i}. py main.py h 1 {hex_x}')
            print(my_x)
            self.assertEqual(0, 0)

    def test_half_ops(self):
        print('test_half_ops')
        for i in range(100):
            hex_x, my_x, py_x = gen_half_float()
            hex_y, my_y, py_y = gen_half_float()

            for act in '+-*/':
                print(f'{i}. py main.py f 1 {hex_x} {act} {hex_y}')
                if act == '/' and py_y == 0:
                    py_z = '+-inf'
                else:
                    py_z = f'{round(eval(f"py_x {act} py_y"), 3):.3f}'
                print('py:', py_x, act, py_y, '=', py_z)
                my_z = eval(f'my_x {act} my_y')
                print('my:', my_x, act, my_y, '=', my_z)
                print()
                self.assertEqual(0, 0)


if __name__ == '__main__':
    unittest.main()
