import math
import decimal


def approx_denver(n):
    i = 1
    x = 1
    delta0 = 1/10**n

    iterations = 0
    while i <= n:
        a = math.pow(x, 1+delta0)
        delta = 1/10**i
        if (a/x-1) < delta0:
            # print('below')
            x += delta
        else:
            # print('above')
            x -= delta
            i = i+1

        iterations += 1

    return x, iterations


def approx_decimal(n):
    decimal.getcontext().prec = 50

    ONE = decimal.Decimal(1)
    TEN = decimal.Decimal(10)

    i = ONE
    x = ONE
    delta0 = ONE/TEN**n

    iterations = 0

    while i <= n:
        a = x ** (ONE+delta0)
        delta = ONE/TEN**i
        if (a/x-ONE) < delta0:
            # print('below')
            x += delta
        else:
            # print('above')
            x -= delta
            i += ONE

        iterations += 1

    return x, iterations

    for i in range(1, n):
        factorial *= i
        sum += 1 / factorial

    return sum, n


def error(x):
    if type(x) == float:
        return abs(x - math.e) / math.e
    else:
        # ideally get n digit string from online...here limited by float's math.e anyway
        decimal_e = decimal.Decimal(math.e)
        return round(abs(x - decimal_e) / decimal_e, 10)


for n in range(1, 20):
    for function in [approx_decimal]:
        x, iterations = function(n)

        print('{:0} {:50}  {:.8f} error={:e} {:20}'.format(
            n, function.__name__, x, error(x), iterations))
    print()
    # (print error in scientific notation)