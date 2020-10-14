# functions to interpolate values in lists and arrays

import numpy as np


def refine_array(p0, p1):
    """
    returns an array with higher resolution
    :param p0: 1d numpy array
    :param p1: grid factor
    :return: new interpolated array
    """
    def_f_array = p0
    def_x_array = np.linspace(0, np.size(def_f_array), np.size(def_f_array))
    def_grid_f = p1
    def_y_len = np.size(def_x_array) + (np.size(def_x_array) - 1) * def_grid_f
    def_x_intrp = np.linspace(np.min(def_x_array), np.max(def_x_array), def_y_len)
    def_y_intrp = np.interp(def_x_intrp, def_x_array, def_f_array)
    return def_y_intrp


def simple_linear(x, p0, p1=999):
    """
    a simple linear interpolator
    :param x: x value
    :param p0: 2D list with the x-y curve relationship
    :param p1: default value to return in case of x off the x-y relationship
    :return: y of x
    """
    try:
        x = x
        rlt = p0
        xmax = max(rlt[0])
        xmin = min(rlt[0])
        if x == xmax:
            i = rlt[0].index(xmax)
            y = rlt[1][i]
        elif x > xmax:
            y = p1
        elif x < xmin:
            y = p1
        else:
            # initial conditions:
            i = 0
            x2 = rlt[0][i]  # higher bound
            # scanning loop:
            while x >= x2:
                i = i + 1
                x2 = rlt[0][i]
            x1 = rlt[0][i - 1]
            y2 = rlt[1][i]
            y1 = rlt[1][i - 1]
            y = ((x - x1) * (y2 -y1) / (x2 - x1)) + y1  # by triangle similarity
            # print('linear interpolation to find x = {}'.format(x))
            # print('x2 = {} in i = {}, x1 = {}, y2 = {}, y1 = {}'.format(x2, i, x1, y2, y1))
    except IndexError:
        y = p1
    return y

'''
r = [[0, 2,  4,  6,  9,  11, 15, 29, 31, 45, 60],
     [0, 20, 37, 60, 65, 74, 81, 95, 97, 99, 100]]
while True:
    v1 = int(input('\nEnter x number: '))
    v2 = simple_linear(x=v1, p0=r, p1=999)
    print('\nThe y of {} is {}'.format(v1, v2))
'''
