import sys


def my_round(b: int) -> str:
    if b != 0:
        sign = b / abs(b)
    else:
        sign = 1
    b = str(abs(b))
    if (len(b) < 4 or int(b[~B + 3]) < 5 or int(b[~B + 3]) == 5 and set(b[~B + 4:]) - {'0'} == {}
            and b[~B + 2] in '02468'):
        return ('-' if sign == -1 else '') + b[:~B + 3].zfill(4)
    else:
        b = b[:~B + 3]
        b = str(int(b) + 1).zfill(4)
        return ('-' if sign == -1 else '') + b


def to_dec(bin_num):
    n = 0
    base = 5
    for i in bin_num[-B:]:
        n = (n + int(i) * base) * 10
        base *= 5

    base = 10 ** (B + 1)
    for i in bin_num[1:-B][::-1]:
        n += int(i) * base
        base <<= 1

    if bin_num[0] == '1':
        n -= base

    n = my_round(n)
    return n[:-3] + '.' + n[-3:]


class FixedPoint:
    def __init__(self, num):
        if isinstance(num, str):
            if num[:2] == '0b':
                self.bin_num = num[2:]
            else:
                self.bin_num = bin(eval(num))[2:]
        elif isinstance(num, int):
            self.bin_num = bin(num)[2:]
        else:
            raise TypeError('Wrong format of fixed-floating number')
        self.bin_num = self.bin_num.zfill(sum(FORMAT))[~sum(FORMAT):]

    def __str__(self):
        return to_dec(self.bin_num)

    def __add__(self, other):  # Операция +
        c = (int(self) + int(other)) & (1 << (A + B)) - 1
        return FixedPoint(c)

    def __sub__(self, other):  # Операция -
        other = ~other + FixedPoint(1)
        return self + other

    def __mul__(self, other):  # Операция *
        a, b = self.bin_num, other.bin_num
        c = int(a, 2) * int(b, 2)
        # print('bin_self:', a)
        # print('bin_other:', b)
        # print('dec c:', c)
        c = bin(c)[2:].zfill(A + A + B + B)
        # print('bin c:', c)

        # (0000_0000) 0000_0001_0000_0000 (0000_0000)
        if c[-B] == '0' or c[-B] == '1' and all(i == '0' for i in c[-B + 1:]) and c[-B - 1] == '0':
            c = c[:-B].zfill(A + A + B)
        else:
            c = bin(int(c[:-B], 2) + 1)[2:].zfill(A + A + B)
        # print('cut_right + circle + zfilled:', c)

        c = c[-(A + B):]
        # print('cut_left (to A+B bites):', c)
        c = FixedPoint('0b' + c)
        # print(c, [c])
        return c

    def __truediv__(self, other):  # Операция /
        a = int(self) * 2 ** (B * 2)
        b = int(other)
        # print(bin(a)[2:].zfill(A + B * 3))
        # print(bin(b)[2:].zfill(A + B))
        c = a // b
        c = bin(c)[2:].zfill(A + B + B)
        # print(c)

        # 0000_0001_0000_0000 (0000_0000)
        # ---------------------^---------
        #                     -B
        if c[-B] == '0' or c[-B] == '1' and all(i == '0' for i in c[-B + 1:]) and c[-B - 1] == '0':
            c = c[:-B].zfill(A + B)
        else:
            c = bin(int(c[:-B], 2) + 1)[2:].zfill(A + B)
        # print(c)

        return FixedPoint('0b' + c)

    def __invert__(self):
        x = FixedPoint(int(''.join(['10'[int(i)] for i in self.bin_num]), 2))
        return x

    def __repr__(self):
        return f'<0b{self.bin_num[:-B]}.{self.bin_num[-B:]} - {to_dec(self.bin_num)}>'

    def __eq__(self, other):
        return self.bin_num == other.bin_num

    def __int__(self):
        return int(self.bin_num, 2)


# class Float:
#     def __init__(self, num):
#         if isinstance(num, str):
#             if num[:2] == '0b':
#                 self.bin_num = num[2:]
#             else:
#                 self.bin_num = bin(eval(num))[2:]
#         elif isinstance(num, int):
#             self.bin_num = bin(num)[2:]
#         else:
#             raise TypeError('Wrong format of fixed-floating number')
#
#         self.bin_num = self.bin_num.zfill(sum(FORMAT))[~sum(FORMAT):]
#
#     def __invert__(self):
#         x = FixedPoint(int(''.join(['10'[int(i)] for i in self.bin_num]), 2))
#         return x
#
#
# class Half:


# FORMAT = (8, 8)
if __name__ == '__main__':
    FORMAT, rounding_type, *args = map(str, sys.argv[1:])
    # print(FORMAT, rounding_type, args)

    if rounding_type != '1':
        print('Wrong rounding type')
        exit(0)

    if '.' in FORMAT:
        A, B = FORMAT = tuple(map(int, FORMAT.split('.')))
        if len(args) == 1:
            a = FixedPoint(args[0])
            print(a)
        else:
            a, sign, b = args
            a = FixedPoint(a)
            # print(a, [a])
            b = FixedPoint(b)
            # print(b, [b])
            if int(b) == 0 and sign == '/':
                print('error')
                exit(0)
            c = eval(f'a {sign} b')
            print(c)

    # elif FORMAT == 'f':
    #     if len(args) == 1:
    #         a = Float(args[0])
    #         print(a)
    #     else:
    #         a, sign, b = args
    #         a = Float(a)
    #         print(a, [a])
    #         b = Float(b)
    #         print(b, [b])
    #         if int(b) == 0 and sign == '/':
    #             print('error')
    #             exit(0)
    #         c = eval(f'a {sign} b')
    #         print(c, [c])
    #
    # elif FORMAT == 'h':
    #     if len(args) == 1:
    #         a = Float(args[0])
    #         print(a)
    #     else:
    #         a, sign, b = args
    #         a = Float(a)
    #         print(a, [a])
    #         b = Float(b)
    #         print(b, [b])
    #         if int(b) == 0 and sign == '/':
    #             print('error')
    #             exit(0)
    #         c = eval(f'a {sign} b')
    #         print(c, [c])

    else:
        print('Wrong format')

    # print(format, round, args)
    # n = FixedPoint(100)
    # for i in range(10000):
    #     if i % 2 ** 8 == 0:
    #         print('AAA')
    #     n = n - FixedPoint(8)
    #     # print([n])
    #     print(n)

'''
16.12 1 0x17360
8.8 1 0xdc9f + 0xd736
8.8 1 0x300 * 0x500
f 1 0xB9CD542
f 1 0x414587dd * 0x42ebf110
h 1 0x4145 * 0x42eb
f 1 0x1 / 0x0

'''
