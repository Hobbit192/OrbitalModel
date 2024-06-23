from math import log10

def standard(integer):
    exponent = int(log10(integer))
    mantissa = integer / (10**exponent)
    return mantissa, exponent

print(standard(1928312378489))
print(type(standard(1)))

