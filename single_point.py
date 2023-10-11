from math import ceil


class Single:
    INF = 'inf'
    NINF = '-inf'
    INFS = {INF, NINF}
    NAN = 'nan'

    SIGN = 1
    EXP = 8
    MAN = 23
    BITES = SIGN + EXP + MAN
    MIN_EXP = -127
    MAX_EXP = 128
    A = 1
    B = MAN
    NULL_VALUE = '0x00000000'
    NULL = '0x0.000000p+0'
    NNULL = '-0x0.000000p+0'
    NULLS = {NULL, NNULL}

    def __init__(self, bin_num: str):
        """Должно подаваться ровно self.BITES бита, т.к. знак, экспонента и мантисса"""

        if bin_num == 'nan':
            bin_num = '1' * self.BITES
        elif bin_num == 'inf':
            bin_num = '0' + '1' * self.EXP + '0' * self.MAN
        elif bin_num == '-inf':
            bin_num = '1' + '1' * self.EXP + '0' * self.MAN

        if bin_num[:2] == '0x':
            bin_num = bin(eval(bin_num))[2:].zfill(self.BITES)
        if bin_num[:2] == '0b':
            bin_num = bin_num[2:]
        assert len(bin_num) == self.BITES
        self.bin_num = bin_num

        self.sign = int(bin_num[0], 2)
        exp = bin_num[1:self.EXP + 1]
        self.exp = int(exp, 2) + self.MIN_EXP
        if self.exp == self.MIN_EXP:
            self.man = int('0' + bin_num[self.EXP + 1:], 2)
        elif self.exp == self.MAX_EXP:
            if set(bin_num[self.EXP + 1:]) == {'0'}:
                self.man = int('0' + bin_num[self.EXP + 1:], 2)
            else:
                self.man = int('1' + bin_num[self.EXP + 1:], 2)
        else:
            self.man = int('1' + bin_num[self.EXP + 1:], 2)

    def __str__(self):
        s = '-' * self.sign
        if self.exp == self.MAX_EXP:
            if self.man == 0:
                if self.sign:
                    return self.NINF
                else:
                    return self.INF
            return self.NAN
        elif self.exp == self.MIN_EXP:
            s += '0x0.'
            if self.man == 0:
                return s + '0' * ceil(self.MAN / 4) + '+0'
        else:
            s += '0x1.'
        # print(self.man)
        # print(bin(self.man))
        # print(bin(self.man)[2:].zfill(self.MAN + 1))
        # print(bin(self.man)[2:][1:])
        man = bin(self.man)[2:].zfill(self.MAN + 1)[1:]
        # print(man)
        for i in range(0, self.MAN, 4):
            s += hex(int(man[i:i + 4].zfill(4), 2))[2:]
        exp = str(self.exp)
        if self.exp >= 0:
            exp = '+' + exp
        s += 'p' + exp
        return s

    def __add__(self, other):
        if str(self) == self.NAN or str(other) == self.NAN:
            return self.__class__(self.NAN)
        if str(self) in self.INFS and str(other) in self.INFS:
            if str(self) != str(other):
                return self.__class__(self.NAN)
            return self

        if str(self) in self.INFS:
            return self

        a = int(self)
        b = int(other)

        sign = int(a + b != abs(a + b))

        print('a:', bin(a))
        print('b:', bin(b))
        c = abs(a + b)
        c = bin(c)[2:]
        print('c:', c)

        if c == '0':
            return self.__class__(self.NULL_VALUE)

        rounded_c = bin_round(c, self.MAN + 1)[1:]
        # print('cut:', len(rounded_c))
        exp = len(c) - len(rounded_c) + 1
        print('exp:', exp)
        print('r: ', rounded_c)  # str(sign) + ' ' + bin(exp)[2:].zfill(self.EXP) + ' ' +

        if exp >= 2 ** self.EXP - 1:
            return self.__class__('inf')
        if exp < 1:
            return self.__class__('-inf')

        c = f'{sign} {bin(exp)[2:].zfill(self.EXP)} {rounded_c}'
        print(c)
        return self.__class__(c.replace(' ', ''))

    def __sub__(self, other):
        if str(self) == self.NAN or str(other) == self.NAN:
            return self.__class__(self.NAN)
        return self + -other

    def __mul__(self, other):
        sign = self.sign ^ other.sign

        a, b = str(self), str(other)
        if a == self.NAN or b == self.NAN:
            return self.__class__(self.NAN)
        if a in self.NULLS and b in self.INFS or a in self.INFS and b in self.NULLS:
            return self.__class__(self.NAN)
        if self.INFS & {a, b}:
            if sign:
                return self.__class__(self.NINF)
            else:
                return self.__class__(self.INF)

        man = self.man * other.man
        man = bin(man)[2:].zfill(self.A + self.A + self.B + self.B)

        if man[0] == '1':
            k = 1
        else:
            man = man[1:]
            k = 0

        man = bin_round(man, self.A + self.B)
        # FIXME: assert len(man) == 24

        exp = (self.exp + other.exp) - self.MIN_EXP + k
        # print(exp)
        if exp >= 2 ** self.EXP - 1:
            return self.__class__('inf')
        if exp < 1:
            return self.__class__('-inf')

        return self.__class__(f'{sign}{bin(exp)[2:].zfill(self.EXP)[:self.EXP]}{man[1:].zfill(self.MAN)[:self.MAN]}')

    def __truediv__(self, other):
        sign = self.sign ^ other.sign

        a, b = str(self), str(other)
        if a == self.NAN or b == self.NAN:
            return self.__class__(self.NAN)
        if a in self.NULLS and b in self.NULLS:
            return self.__class__(self.NAN)
        if a in self.INFS and b in self.INFS:
            return self.__class__(self.NAN)
        if str(other) in self.NULLS:
            if sign:
                return self.__class__(self.NINF)
            else:
                return self.__class__(self.INF)

        man_a = self.man * 2 ** (self.B * 2)
        man_b = other.man

        man = man_a // man_b
        man = bin(man)[2:].zfill(self.A + self.B + self.B)

        man = bin_round(man, -self.B)
        # FIXME: assert len(man) == 24

        exp = (self.exp - other.exp) - self.MIN_EXP
        if exp >= 2 ** self.EXP - 1:
            return self.__class__('inf')
        if exp < 1:
            return self.__class__('-inf')
        exp = bin(exp)[2:].zfill(self.EXP)

        return self.__class__(f'{sign}{exp[:self.EXP]}{man[1:].zfill(self.MAN)[:self.MAN]}')

    def __neg__(self):
        return self.__class__(str(self.sign ^ 1) + self.bin_num[1:])

    def __repr__(self):
        return (f'<{hex(int(self.bin_num, 2))}: {self.sign} {bin(self.exp - self.MIN_EXP)[2:].zfill(self.EXP)} '
                f'{bin(self.man)[2:].zfill(self.MAN)[1:]}>')

    def __float__(self):
        return self.man * 2 ** (self.exp - self.MAN) * int('-' * self.sign + '1') * 1.0

    def __int__(self):
        return int('-' * self.sign + '1') * self.man * 2 ** (self.exp - self.MIN_EXP)

    def __index__(self):
        return int(self.bin_num, 2)


def bin_round(num: str, o: int):
    if len(num) <= o or num[o] == '0' or num[o] == '1' and set(num[o + 1:]) - {'0'} == set() and num[o - 1] == '0':
        return num[:o]
    else:
        return bin(int(num[:o], 2) + 1)[2:]
