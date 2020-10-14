# bunch of list and tuple useful entry functions
from tools import validate


def list_1d_float(p0=5, p1='Field', p2=True, clr=True):
    """
    Input a 1D array of float numbers
    :param p0: size of array
    :param p1: label of elements
    :param p2: boolean to print index starting from 1
    :return: 1D list
    """
    r1_inpt = list()
    if p2:
        for i in range(0, p0):
            print('>> {} {}: '.format(p1, i + 1))
            v0_inpt = validate.flt(clr=clr)
            r1_inpt.append(v0_inpt)
    else:
        for i in range(0, p0):
            print('>> {} {}: '.format(p1, i))
            v0_inpt = validate.flt(clr=clr)
            r1_inpt.append(v0_inpt)
    return r1_inpt


def list_1d_pstv_flt(p0=5, p1='Field', p2=True, clr=True, p3=1, p4=0, p5=3):
    """
    Input a 1D array of float numbers
    :param p0: size of array
    :param p1: label of elements
    :param p2: boolean to print index starting from 1
    :param p3: A parameter for linear transf. on index (Ax + B)
    :param p4: B parameter for linear transf. on index (Ax + B)
    :param p5: decimal plates
    :return: 1D list
    """
    r1_inpt = list()
    if p2:
        for i in range(0, p0):
            y = (p3 * i) + p4
            print('>> {} {}: '.format(p1, y + 1))
            v0_inpt = validate.positive_flt(clr=clr)
            r1_inpt.append(round(v0_inpt, p5))
    else:
        for i in range(0, p0):
            y = (p3 * i) + p4
            print('>> {} {}: '.format(p1, y))
            v0_inpt = validate.positive_flt(clr=clr)
            r1_inpt.append(round(v0_inpt, p5))
    return r1_inpt


def list_1d_pstv_asc_flt(p0=5, p1='Field', p2=True, clr=True, p3=1, p4=0, p5=3):
    """
    Input a 1D array of positive ascending float numbers
    :param p0: size of array
    :param p1: label of elements
    :param p2: boolean to print index starting from 1
    :param p3: A parameter for linear transf. on index (Ax + B)
    :param p4: B parameter for linear transf. on index (Ax + B)
    :param p5: decimal plates
    :return: 1D list
    """
    r1_inpt = list()
    if p2:
        for i in range(0, p0):
            y = (p3 * i) + p4
            print('>> {} {}: '.format(p1, y + 1))
            if i == 0:
                v0_inpt = validate.positive_flt(clr=clr)
            else:
                v0_inpt = validate.flt_hithan(p0=r1_inpt[i - 1], clr=clr)
            r1_inpt.append(round(v0_inpt, p5))
    else:
        for i in range(0, p0):
            y = (p3 * i) + p4
            print('>> {} {}: '.format(p1, y))
            if i == 0:
                v0_inpt = validate.positive_flt(clr=clr)
            else:
                v0_inpt = validate.flt_hithan(p0=r1_inpt[i - 1], clr=clr)
            r1_inpt.append(round(v0_inpt, p5))
    return r1_inpt


def list_2d_float(p0=3, p1=3, p2='Record', p3='Field', p4=True, clr=True):
    """
    Input a 2D mutable matrix of float numbers
    :param p0: number of lines (records)
    :param p1: number of columns (fields)
    :param p2: label for lines
    :param p3: label for columns
    :param p4: boolean to print index starting from 1
    :return: 2D list
    """
    r1_inpt = list()  # records
    m1_inpt = list()  # matrix
    if p4:
        for i in range(0, p0):
            print('>> {} {}: '.format(p2, i + 1))
            for j in range(0, p1):
                print('\t >> {} {} >> {} {}\n\t'.format(p2, i + 1, p3, j + 1), end='')
                v0_inpt = validate.flt(clr=clr)
                r1_inpt.append(v0_inpt)
            m1_inpt.append(r1_inpt[:])
            r1_inpt.clear()
    else:
        for i in range(0, p0):
            print('>> {} {}: '.format(p2, i))
            for j in range(0, p1):
                print('\t >> {} {} >> {} {}\n\t'.format(p2, i, p3, j), end='')
                v0_inpt = validate.flt(clr=clr)
                r1_inpt.append(v0_inpt)
            m1_inpt.append(r1_inpt[:])
            r1_inpt.clear()
    return m1_inpt


def tuple_1d_float(p0=5, p1='Field', p2=True, clr=True):
    """
    Input a 1D immutable array of float numbers
    :param p0: size of array
    :param p1: label of elements
    :param p2: boolean to print index starting from 1
    :return: 1D tuple
    """
    r1_inpt = list()
    if p2:
        for i in range(0, p0):
            print('>> {} {}: '.format(p1, i + 1))
            v0_inpt = validate.flt(clr=clr)
            r1_inpt.append(v0_inpt)
    else:
        for i in range(0, p0):
            print('>> {} {}: '.format(p1, i))
            v0_inpt = validate.flt(clr=clr)
            r1_inpt.append(v0_inpt)
    return tuple(r1_inpt)


def tuple_2d_float(p0=3, p1=3, p2='Record', p3='Field', p4=True):
    """
    Input a 2D immutable matrix of float numbers
    :param p0: number of lines (records)
    :param p1: number of columns (fields)
    :param p2: label for lines
    :param p3: label for columns
    :param p4: boolean to print index starting from 1
    :return: 2D tuple
    """
    r1_inpt = list()  # records
    m1_inpt = list()  # matrix
    if p4:
        for i in range(0, p0):
            print('>> {} {}: '.format(p2, i + 1))
            for j in range(0, p1):
                print('\t >> {} {} >> {} {}\n\t'.format(p2, i + 1, p3, j + 1), end='')
                v0_inpt = validate.flt()
                r1_inpt.append(v0_inpt)
            m1_inpt.append(tuple(r1_inpt[:]))
            r1_inpt.clear()
        tp1_inpt = tuple(m1_inpt)
    else:
        for i in range(0, p0):
            print('>> {} {}: '.format(p2, i + 1))
            for j in range(0, p1):
                print('\t >> {} {} >> {} {}\n\t'.format(p2, i, p3, j), end='')
                v0_inpt = validate.flt()
                r1_inpt.append(v0_inpt)
            m1_inpt.append(tuple(r1_inpt[:]))
            r1_inpt.clear()
        tp1_inpt = tuple(m1_inpt)
    return tp1_inpt


'''
v = list_1d_float()
print(v)
x = list_2d_float()
print(x)
y = tuple_2d_float()
print(y)
'''
