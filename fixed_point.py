class FixedPoint:
    A = 16
    B = 16

    def __init__(self, num):
        if num[:2] == '0x':
            num = bin(eval(num))
        self.bin_num = num[2:].zfill(self.A + self.B)

    def __str__(self):
        bin_num = self.bin_num
        n = 0
        base = 5
        for i in bin_num[len(bin_num) - self.B:]:
            n = (n + int(i) * base) * 10
            base *= 5

        base = 10 ** (self.B + 1)
        for i in bin_num[1:len(bin_num) - self.B][::-1]:
            n += int(i) * base
            base <<= 1
        n -= int(bin_num[0]) * base

        n = self.my_round(n)
        return n[:-3] + '.' + n[-3:]

    def __add__(self, other):  # Операция +
        c = (int(self) + int(other)) & (1 << (self.A + self.B)) - 1
        return FixedPoint(bin(c))

    def __sub__(self, other):  # Операция -
        other = ~other + FixedPoint(bin(1))
        return self + other

    def __mul__(self, other):  # Операция *
        a, b = self.bin_num, other.bin_num
        c = int(a, 2) * int(b, 2)
        c = bin(c)[2:].zfill(self.A + self.A + self.B + self.B)

        o = -self.B
        if c[o] == '0' or c[o] == '1' and (self.B == 1 or set(c[o + 1:]) - {'0'} == set()) and c[o - 1] == '0':
            c = c[:len(c) + o].zfill(self.A + self.B)
        else:
            c = bin(int(c[:len(c) + o], 2) + 1)[2:].zfill(self.A + self.B)

        c = c[-(self.A + self.B):]
        c = FixedPoint('0b' + c)
        return c

    def __truediv__(self, other):  # Операция /
        if other == FixedPoint('0x0'):
            return 'error'
        a = int(self) * 2 ** (self.B * 2)
        b = int(other)
        c = a // b
        c = bin(c)[2:].zfill(self.A + self.B + self.B)

        # 0000_0001_0000_0000 (0000_0000)
        # ---------------------^---------
        #                     -o
        o = -self.B
        if c[o] == '0' or c[o] == '1' and set(c[o + 1:]) - {'0'} == set() and c[o - 1] == '0':
            c = c[:len(c) + o].zfill(self.A + self.B)
        else:
            c = bin(int(c[:len(c) + o], 2) + 1)[2:].zfill(self.A + self.B)

        return FixedPoint('0b' + c)

    def __invert__(self):
        return FixedPoint('0b' + ''.join('10'[int(i)] for i in self.bin_num))

    def __repr__(self):
        return f'<0b{self.bin_num[:-self.B]}.{self.bin_num[-self.B:]} - {int(self)} - {str(self)}>'

    def __eq__(self, other):
        return self.bin_num == other.bin_num

    def __int__(self):
        return int(self.bin_num, 2)

    def __float__(self):
        return float(str(self))

    @staticmethod
    def my_round(n: int) -> str:
        sign = '-' * (n != abs(n))
        n = str(abs(n))

        if FixedPoint.B < 3:
            return sign + (n + '0' * (2 - FixedPoint.B)).zfill(4)

        n = n.zfill(max(FixedPoint.B + 1, 4))
        o = ~FixedPoint.B + 3
        if len(n) < 4 or int(n[o]) < 5 or int(n[o]) == 5 and set(n[o + 1:]) - {'0'} == set() and n[o - 1] in '02468':
            return sign + n[:o].zfill(4)
        else:
            n = n[:o]
            n = str(int(n) + 1).zfill(4)
            return sign + n
