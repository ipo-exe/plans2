# ________________________________________________________________________
#       UFRGS - UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL
#           IPH - INSTITUTO DE PESQUISAS HIDRAULICAS
#
#     Research Group in Water Resources Management and Planning - WARP
#                    https://www.ufrgs.br/warp
#           Porto Alegre, Rio Grande do Sul, Brazil
# ________________________________________________________________________
#
# Author: IPORA BRITO POSSANTTI, Environmental Engineer
# Contact: possantti@gmail.com
# Date: November of 2019
# Description:
#               this package contains a set of custom functions for display data on screen


from tools import color, stringsf
from time import sleep


def str_title_clr(p0, clr=False, clrid='bldwhite'):
    if clr:
        if clrid == 'bldwhite':
            print(color.bldwhite(stringsf.title(p0)))
        elif clrid == 'bldgreen':
            print(color.bldgreen(stringsf.title(p0)))
        else:
            print(stringsf.title(p0))
    else:
        print(stringsf.title(p0))


def str_subtitle_clr(p0, clr=False, clrid='bldwhite'):
    if clr:
        if clrid == 'bldwhite':
            print(color.bldwhite(stringsf.subtitle(p0)))
        elif clrid == 'bldgreen':
            print(color.bldgreen(stringsf.subtitle(p0)))
        else:
            print(stringsf.subtitle(p0))
    else:
        print(stringsf.subtitle(p0))


def mtx_1d_float(p0, p1='Field', p2='Elements', p3=1, p4='Title', p6=1, p7=0, clr=False):
    """
    fancy display of 1d list of float values. p5 is deprecated
    :param p0: list to display
    :param p1: label for columns
    :param p2: label for row
    :param p3: decimal plates for float values
    :param p4: label for title
    :param clr: color boolean control
    :param p6: A param. to linear transf. on index
    :param p7: B param to linear transf. on index
    :return: none
    """
    # get parameters:
    while True:
        a = len(p2) + 2
        h = p1 + ' ' + (str(len(p0) + 1))
        b = len(stringsf.center(h, p1=6)) + 2
        if b < len(str(round(max(p0), p3))):
            b = len(str(round(max(p0), p3))) + 2
        c = a + (b*len(p0))
        break
    # header:
    while True:
        # printing upper line
        print('_' * c)
        # printing header
        if clr:
            print(color.bldwhite(stringsf.center(p4.upper(), (a + (b * len(p0))))))
        else:
            print(stringsf.center(p4.upper(), (a + (b * len(p0)))))
        print('{}'.format(' ' * a), end='')
        for i in range(0, len(p0)):
            i_aux1 = (p6 * i) + p7  # linear transformation on index
            s = p1 + ' ' + str(int(i_aux1))
            if clr:
                print(color.bldwhite(stringsf.center(s, b)), end='')
            else:
                print(stringsf.center(s, b), end='')
        print()
        break
    # elements:
    while True:
        if clr:
            print(color.bldwhite(stringsf.center(p2, p1=a)), end='')
        else:
            print(stringsf.center(p2, p1=a), end='')
        for i in range(0, len(p0)):
            if clr:
                print(color.bldgreen(stringsf.center(str(round(p0[i], p3)), p1=b)), end='')
            else:
                print(stringsf.center(str(round(p0[i], p3)), p1=b), end='')
        print()
        break
    print('_' * c)


def mtx_2d_float(p0, p1='Fld', p2='Rcrd', p3=1, p4='Flds', p5='Records',
                 p6=1.0, p7=0.0, p9='Title', p10=True, p11=1, p12=0, clr=False):
    """
    This function prints on screen a matrix of float numbers in a fancy way
    p8 is deprecated.
    :param p0: 2D list containing matrix
    :param p1: minor label for columns
    :param p2: minor label for lines
    :param p3: decimal plates of float numbers
    :param p4: major label for columns
    :param p5: major label for lines
    :param p6: A parameter for linear index transformation
    :param p7: B parameter for linear index transformation
    :param p9: title of matrix
    :param p10: boolean to set sleep time on printing
    :param p11: default header sleep time
    :param p12: decimal plates for labels
    :param clr: boolean to control coloring
    :return: no return
    """
    # getting some sizing parameters:
    while True:
        # get A parameter:
        while True:
            a = len(p5)
            # check if sub labels will overflow space:
            aux_f1 = (len(p0) * p6) + p7  # linear transform on max index
            aux_s1 = p2 + ' ' + str(round(aux_f1, p3))
            if len(aux_s1) > a:
                a = len(aux_s1)
            break
        # get B parameter:
        while True:
            aux_f1 = (len(p0) * p6) + p7  # linear transform on max index
            aux_s1 = p1 + ' ' + (str(round(aux_f1, p3)))
            b = len(stringsf.center(aux_s1))
            break
        # get C parameter:
        while True:
            c = a + (b * len(p0[0]))
            break
        # scanning all matrix line by line to find longest element:
        for i in range(0, len(p0)):
            if b < len(str(round(max(p0[i]), p3))):
                b = len(str(round(max(p0[i]), p3))) + 2
        break
    # header:
    while True:
        # printing upper line:
        print('_' * c)
        # printing title:
        if clr:
            print(color.bldwhite(stringsf.center(p9.upper(), c)))
        else:
            print(stringsf.center(p9.upper(), c))
        # printing upper header:
        if clr:
            aux_s2 = color.bldwhite(stringsf.center(p5, a))
            aux_s3 = color.bldwhite(stringsf.center(p4, (c - a)))
        else:
            aux_s2 = stringsf.center(p5, a)
            aux_s3 = stringsf.center(p4, (c - a))
        print('{}{}'.format(aux_s2, aux_s3))
        # printing sub header
        print(' ' * a, end='')
        for i in range(0, len(p0[0])):
            aux_f1 = (i * p6) + p7  # linear transformation on label
            aux_s4 = p1 + ' ' + str(round(aux_f1, p12))
            if p12 == 0:
                aux_s4 = p1 + ' ' + str(int(aux_f1))
            if clr:
                print(color.bldwhite(stringsf.center(aux_s4, b)), end='')
            else:
                print(stringsf.center(aux_s4, b), end='')
        print()
        break
    if p10:
        sleep(p11)
    # elements:
    while True:
        for i in range(0, len(p0)):
            aux_f1 = (i * p6) + p7  # linear transformation on label
            aux_s4 = p2 + ' ' + str(round(aux_f1, p12))
            if p12 == 0:
                aux_s4 = p2 + ' ' + str(int(aux_f1))
            if clr:
                print(color.bldwhite(stringsf.center(aux_s4, a)), end='')
            else:
                print(stringsf.center(aux_s4, a), end='')
            for j in range(0, len(p0[i])):
                if clr:
                    print(color.bldgreen(stringsf.center(str(round(p0[i][j], p3)), b)), end='')
                else:
                    print(stringsf.center(str(round(p0[i][j], p3)), b), end='')
            print()
            if p10:
                sleep(p11/3)
        break
    # final line:
    print('_' * (a + (b * len(p0[0]))))


def mtx_2d_float_simple(p0, p1='Matrix'):
    print('\n{}: '.format(p1))
    for i in range(0, len(p0)):
        print('\t{}'.format(p0[i]))


def mtx_3d_float_simple(p0, p1='Matrix'):
    print('\n{}: '.format(p1))
    for i in range(0, len(p0)):
        print('item {}:'.format(i))
        for j in range(0, len(p0[i])):
            print('\t{}'.format(p0[i][j]))


def rlt_2d_float(p0, p1, p2='Rcrd', p3=1, p5='Records',
                 p6=1.0, p7=0, p8=True, p9='Title', p10=False, p11=1, clr=False):
    """
    This function prints on screen a 2D relation of float numbers in a fancy way
    Therefore it must receive a list of header labels (p1)
    Parameter p4 does not exist here.
    :param p0: 2D list containing matrix
    :param p1: list of minor labels for columns
    :param p2: minor label for lines
    :param p3: decimal plates of float numbers
    :param p5: major label for lines
    :param p6: A parameter for linear index transformation
    :param p7: B parameter for linear index transformation
    :param p8: boolean to set index starting in 1 (True) or 0 (False)
    :param p9: title of matrix
    :param p10: boolean to set sleep time on printing
    :param p11: default header sleep time
    :param clr: boolean to control coloring
    :return: no return
    """
    # getting some sizing parameters:
    while True:
        # get A parameter:
        while True:
            a = len(p5)
            # check if sub labels will overflow space:
            aux_f1 = (len(p0) * p6) + p7  # linear transform on max index
            aux_s1 = p2 + ' ' + str(round(aux_f1, p3))
            if len(aux_s1) > a:
                a = len(aux_s1)
            break
        # get B parameter:
        while True:
            aux_f1 = (len(p0) * p6) + p7  # linear transform on max index
            aux_i1 = 0
            aux_s1 = ''
            for i in range(0, len(p1)):
                if len(p1[i]) > aux_i1:
                    aux_i1 = len(p1[i])
                    aux_s1 = p1[i]
            aux_s1 = aux_s1 + ' ' + (str(round(aux_f1, p3)))
            b = len(stringsf.center(aux_s1))
            break
        # get C parameter:
        while True:
            c = a + (b * len(p1))
            break
        # scanning all matrix line by line to find longest element:
        for i in range(0, len(p0)):
            if b < len(str(round(max(p0[i]), p3))):
                b = len(str(round(max(p0[i]), p3))) + 2
        break
    # header:
    while True:
        # printing upper line:
        print('_' * c)
        # printing title:
        if clr:
            print(color.bldwhite(stringsf.center(p9.upper(), (a + (b * len(p1))))))
        else:
            print(stringsf.center(p9.upper(), (a + (b * len(p1)))))
        # printing header:
        aux_s2 = stringsf.center(p5, a)
        if clr:
            print('{}'.format(color.bldwhite(aux_s2)), end='')
        else:
            print('{}'.format(aux_s2), end='')
        for i in range(0, len(p1)):
            aux_s4 = p1[i]
            if clr:
                print(color.bldwhite(stringsf.center(aux_s4, b)), end='')
            else:
                print(stringsf.center(aux_s4, b), end='')
        print()
        break
    if p10:
        sleep(p11)
    # elements:
    while True:
        for i in range(0, len(p0)):
            if p8:
                aux_i3 = i + 1
            else:
                aux_i3 = i
            aux_i4 = (aux_i3 * p6) + p7  # linear transformation on label
            aux_s4 = p2 + ' ' + str(round(aux_i4, p3))
            if clr:
                print(color.bldwhite(stringsf.center(aux_s4, a)), end='')
            else:
                print(stringsf.center(aux_s4, a), end='')
            for j in range(0, len(p1)):
                if clr:
                    print(color.bldgreen(stringsf.center(str(round(p0[i][j], p3)), p1=b)), end='')
                else:
                    print(stringsf.center(str(round(p0[i][j], p3)), p1=b), end='')
            print()
            if p10:
                sleep(p11/3)
        break
    # final line:
    # print('_' * c)


def summary(p0, p1='summary', p2=1, p3=False, p4=1, clr=False):
    """
    fancy float variables summary
    :param p0: 2d list with label-variable
    :param p1: title string
    :param p2: decimal plates
    :param p3: boolean to control sleep time
    :param p4: time of sleep
    :param clr: boolean to control coloring
    :return:
    """
    # get sizing parameters:
    while True:
        a = 0
        for i in range(0, len(p0)):
            if len(p0[i][0]) > a:
                a = len(p0[i][0])
        b = 0
        for i in range(0, len(p0)):
            if len(str(round(p0[i][1], p2))) > b:
                b = len(str(round(p0[i][1], p2)))
        c = a + b + 8
        if c < len(p1):
            c = len(p1)
        break
    # print header
    print('\n{}'.format('_'*c))
    if clr:
        print(color.bldwhite(stringsf.center(p0=p1, p1=c).capitalize()))
    else:
        print(stringsf.center(p0=p1, p1=c).capitalize())
    if p3:
        sleep(p4)
    # print elements
    for i in range(0, len(p0)):
        aux_s1 = str(p0[i][0]).lower().capitalize()
        d = c - len(aux_s1) - b
        aux_s2 = '.' * d
        if clr:
            aux_s3 = color.bldgreen(str(round(p0[i][1], p2)))
        else:
            aux_s3 = str(round(p0[i][1], p2))
        if clr:
            print('{}{}{}'.format(color.bldwhite(aux_s1), aux_s2, aux_s3))
        else:
            print('{}{}{}'.format(aux_s1, aux_s2, aux_s3))
        if p3:
            sleep(p4/3)
    # removed bottom line:
    # print('\n{}'.format('_' * c))


def timeseries(p0, p1, p2, p3='time series', p4=False, p5=0.3, clr=False):
    """
    A function that displays time series (first column is time)
    :param p0: 2d list containing data
    :param p1: 1d list of head labels
    :param p2: 1d list of series resolution
    :param p3: title
    :param p4: bool control for sleep time
    :param p5: sleep time
    :param clr: color bool control
    :return:
    """
    # get sizing parameters
    c = 0
    for e in p1:
        c = c + len(str(e)) + 2
    # print header:
    print('\n{}'.format('_'*c))
    if clr:
        print(color.bldwhite(stringsf.center(p0=p3, p1=c).upper()))
    else:
        print(stringsf.center(p0=p3, p1=c).upper())
    if p4:
        sleep(p5)
    # print head labels
    for e in p1:
        aux_str = ' ' + str(e) + ' '
        if clr:
            print(color.bldwhite(aux_str), end='')
        else:
            print(aux_str, end='')
    print()
    if p4:
        sleep(p5)
    # print elements
    for i in range(0, len(p0)):
        for j in range(0, len(p0[i])):
            aux_int = len(str(p1[j])) + 2
            aux_str = stringsf.center(str(round(p0[i][j], p2[j])), p1=aux_int)
            if clr:
                print(color.bldgreen(aux_str), end='')
            else:
                print(aux_str, end='')
        print()
        if p4:
            sleep(p5)


def dict_1d_float(p0, p1='dictionary title', p2=3, clr=False):
    # get sizing parameters:
    a = 0
    for e in p0:
        if len(str(e)) > a:
            a = len(str(e))
    # header
    print(stringsf.title(p1, p3=False))
    h = len(stringsf.title(p1))
    if h > 30:
        h = 30
    if a > h:
        h = h + 5
    # body of data
    for e in p0:
        print(e, end='')
        b = h - len(str(e))
        print('.' * b, end='')
        if clr:
            print('{}'.format(color.bldgreen(str(round(float(p0[e]), p2)))))
        else:
            print('{}'.format(str(round(float(p0[e]), p2))))


def progressbarok(p0=20, clr=False):
    """
    progress bar display
    :param p0: bar size
    :param clr: color boolean control
    :return: none
    """
    if clr:
        for i in range(1, p0):
            print('{}'.format(color.bckgreen(' ')), end='', flush=True)
            sleep(1 / i)
        print(' ' + color.bckgreen('    >>OK    ') + '\n')
    else:
        for i in range(1, p0):
            print('{}'.format('>'), end='', flush=True)
            sleep(1 / i)
        print(' ' + '    >>OK    ' + '\n')
    sleep(1)


def errorinput(p0=' You must enter a valid input!', clr=False):
    """
    error message display
    :param p0: erros message
    :param clr: color boolean control
    :return: none
    """
    if clr:
        errinpt = color.bckred('  >>Error!  ') + ' ' + p0 + '\n'
    else:
        errinpt = '  >>Error!  ' + ' ' + p0 + '\n'
    print(errinpt)
    sleep(0.5)


def okinput(p0='', p1=0.3, clr=False):
    """
    ok input display
    :param p0: message
    :param p1: sleep time in seconds
    :param clr: color boolean control
    :return:
    """
    if clr:
        okinpt = color.bckgreen('    >>OK    ') + ' ' + p0 + '\n'
    else:
        okinpt = '    >>OK    ' + ' ' + p0 + '\n'
    print(okinpt)
    sleep(p1)


def wrnginput(p0='', clr=False):
    """
    warning input display
    :param p0: message string
    :param clr: color boolean control
    :return: none
    """
    if clr:
        wrnginpt = color.bckorage(' >>Warning! ') + ' ' + p0 + '\n'
    else:
        wrnginpt = ' >>Warning! ' + ' ' + p0 + '\n'
    print(wrnginpt)
    sleep(0.5)


def waiting(p0='.', p1='Waiting', p2=0.3, p4=10, clr=False):
    """
    waiting display
    :param p0: marker
    :param p1: msg txt
    :param p2: sleep time in seconds
    :param p4: size
    :param clr: color boolean control
    :return: none
    """
    print('\n')
    if clr:
        print(color.bldgreen(p1), end='')
    else:
        print(p1, end='')
    for i in range(0, p4 + 1):
        if clr:
            print(color.bldgreen(p0), end=' ', flush=True)
            sleep(p2)
        else:
            print(p0, end=' ', flush=True)
            sleep(p2)
    print('\n')


def demo():
    waiting(clr=True)
    okinput(p0='we are good to go', clr=True)
    wrnginput(p0='this is a warning message', clr=True)
    errorinput(clr=True)


#demo()
