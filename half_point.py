from single_point import Single


class Half(Single):
    SIGN = 1
    EXP = 5
    MAN = 10
    BITES = SIGN + EXP + MAN
    MIN_EXP = -15
    MAX_EXP = 16
    A = 1
    B = MAN
    NULL_VALUE = '0x0000'
    NULL = '0x0.000p+0'
    NNULL = '-0x0.000p+0'
    NULLS = {NULL, NNULL}
