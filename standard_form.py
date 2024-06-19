from math import log10


def standard_form(integer):
    exponent = int(log10(integer))
    mantissa = integer / (10 ** exponent)

    return mantissa, exponent
