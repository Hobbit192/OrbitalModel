from math import log10


def standard_form(integer):
    exponent = int(log10(integer))
    mantissa = integer / (10 ** exponent)

    return mantissa, exponent


def round_to_sf(value, significant_figures):
    formatted_value = '{:.{sf}g}'.format(value, sf=significant_figures)
    # Convert to float if there is a decimal point, otherwise to int
    if '.' in formatted_value:
        return float(formatted_value)
    else:
        return int(formatted_value)
