# useful engineering economics functions
import numpy as np


def pval(c, r, n):
    """
    present value function
    :param c: cash in $
    :param r: interest rate
    :param n: number of periods
    :return: present value of cash in $
    """
    pval = c / (pow((1 + r), n))
    return pval


def fval(p, r, n):
    """
    future value function
    :param p: present cash in $
    :param r: interest rate
    :param n: number of periods
    :return: present value of cash in $
    """
    fval = p * (pow((1 + r), n))
    return fval


def fval_array(p, r, n, t):
    """
    future value function
    :param p: present cash in $ in n = 0
    :param r: interest rate
    :param n: number of periods and size of array
    :return: array present value of cash in $
    """
    df_fval = np.zeros(n)
    for df_i in range(0, np.size(df_fval)):
        df_t = df_i * t
        print(df_t)
        df_fval[df_i] = round(fval(p, r, df_t), 2)
    return df_fval



'''
cash = 1000
rate = 0.02
period = 10
pval_cash = pval(cash, rate, period)
print(pval_cash)

p = 1000
r = 0.09
n = 5
f = fval(p, r, n)
print(f)
print(np.zeros(5))
print(fval_array(p, r, 5, 5))
'''


