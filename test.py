import os
import unittest
from main import *
from random import *


def gen_fixed_float(a, b, int_x=None) -> (str, float):
    if int_x is None:
        int_x = randint(0, (1 << (a + b)) - 1)

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
    py_x = float(sign + n[:len(n) - b - 1] + '.' + n[len(n) - b - 1:])

    return hex(int_x), py_x


def gen_single_float() -> (str, float):
    sign = randint(0, 1)
    exp = randint(1, 254)
    man = randint(0, 2 ** 23 - 1)
    py_x = int('-' * sign + '1') * (man + 2 ** 23) * 2 ** (exp - 127)
    h = hex(int(f'{sign}{bin(exp)[2:].zfill(8)}{bin(man)[2:].zfill(23)}', 2))
    return h, py_x


def gen_half_float() -> (str, float):
    sign = randint(0, 1)
    exp = randint(1, 30)
    man = randint(0, 2 ** 10 - 1)
    py_x = int('-' * sign + '1') * (man + 2 ** 10) * 2 ** (exp - 14)
    h = hex(int(f'{sign}{bin(exp)[2:].zfill(5)}{bin(man)[2:].zfill(10)}', 2))
    my_x = Half(h)
    return h, py_x


def read_temp():
    with open('temp.txt') as file:
        return file.read().strip()


class MyTestCase(unittest.TestCase):
    def test_fixed(self):
        print('-' * 20)
        print('test_fixed')
        for i in range(20):
            length = randint(1, 32)
            a = randint(1, length)
            b = length - a
            FixedPoint.A, FixedPoint.B = a, b

            hex_x, py_x = gen_fixed_float(a, b)
            q = f'py main.py {a}.{b} 1 {hex_x}'
            print(f'{i + 1}.', q)
            os.system(q + ' > temp.txt')
            with open('temp.txt') as file:
                ans = file.read().strip()
                print(f'py: {round(py_x, 3):.3f} \t  my:', ans)
                self.assertEqual(f'{py_x:.3f}', ans)
        os.system('del temp.txt')

    def test_fixed_special(self):
        print('-' * 20)
        print('test_fixed_special')
        for i in range(10):
            length = randint(1, 32)
            a = randint(1, length)
            b = length - a
            FixedPoint.A, FixedPoint.B = a, b

            hex_x, py_x = gen_fixed_float(a, b, 0)

            q = f'py main.py {a}.{b} 1 {hex_x}'
            print(f'{i + 1}.', q)
            os.system(q + ' > temp.txt')

            ans = read_temp()
            print('py:', py_x, '\t my:', ans)
            self.assertEqual(f'{py_x:.3f}', ans)
        os.system('del temp.txt')

    def test_fixed_ops(self):
        print('-' * 20)
        print('test_fixed_ops')

        for i in range(5):
            length = randint(1, 32)
            a = randint(1, length)
            b = length - a
            FixedPoint.A, FixedPoint.B = a, b

            hex_x, py_x = gen_fixed_float(a, b)
            hex_y, py_y = gen_fixed_float(a, b)

            for act in '+-*/':
                q = f'py main.py {a}.{b} 1 {hex_x} {act} {hex_y}'
                print(f'{i + 1}.', q)
                os.system(q + ' > temp.txt')
                ans = read_temp()
                if act == '/' and py_y == 0:
                    py_z = 'error'
                else:
                    py_z = eval(f"py_x {act} py_y")
                    py_z = str(round(py_z, 3))
                print(py_x, act, py_y, '=')
                print('py:', py_z)
                print('my:', ans)
                print()
                self.assertEqual(0, 0)
        os.system('del temp.txt')

    def test_single(self):
        print('-' * 20)
        print('test_single')
        for i in range(20):
            hex_x, py_x = gen_single_float()
            q = f'py main.py f 1 {hex_x}'
            print(f'{i + 1}.', q)
            os.system(q + ' > temp.txt')
            ans = read_temp()
            print('my:', ans)
            print('py:', py_x)
            self.assertEqual(0, 0)
        os.system('del temp.txt')

    def test_single_ops(self):
        print('-' * 20)
        print('test_single_ops')
        for i in range(5):
            hex_x, py_x = gen_single_float()
            hex_y, py_y = gen_single_float()

            for act in '+-*/':
                q = f'py main.py f 1 {hex_x} {act} {hex_y}'
                print(f'{i}.', q)
                os.system(q + ' > temp.txt')
                ans = read_temp()
                if act == '/' and py_y == 0:
                    py_z = '+-inf'
                else:
                    py_z = f'{round(eval(f"py_x {act} py_y"), 3):.3f}'
                print(py_x, act, py_y, '=')
                print('py:', py_z)
                print('my:', ans)
                print()
                self.assertEqual(0, 0)
        os.system('del temp.txt')

    def test_half(self):
        print('-' * 20)
        print('test_half')
        for i in range(20):
            hex_x, py_x = gen_half_float()
            q = f'py main.py h 1 {hex_x}'
            print(f'{i + 1}.', q)
            os.system(q + ' > temp.txt')
            ans = read_temp()
            print('my:', ans)
            print('py:', py_x)
            self.assertEqual(0, 0)
        os.system('del temp.txt')

    def test_half_ops(self):
        print('-' * 20)
        print('test_half_ops')

        for i in range(5):
            hex_x, py_x = gen_half_float()
            hex_y, py_y = gen_half_float()

            for act in '+-*/':
                q = f'py main.py h 1 {hex_x} {act} {hex_y}'
                print(f'{i}.', q)
                os.system(q + ' > temp.txt')
                ans = read_temp()
                if act == '/' and py_y == 0:
                    py_z = '+-inf'
                else:
                    py_z = f'{round(eval(f"py_x {act} py_y"), 3):.3f}'
                print(py_x, act, py_y, '=')
                print('py:', py_z)
                print('my:', ans)
                print()
                self.assertEqual(0, 0)
        os.system('del temp.txt')


if __name__ == '__main__':
    unittest.main()
