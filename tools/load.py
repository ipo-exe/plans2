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
# Date: March of 2020
# Description:
#               this package contains code to load data to plans

import pandas as pd
from tools import display, stringsf


def serie_chuva_hidroweb(p0):
    f = p0
    fle = open(f, 'r')
    lst = fle.readlines()[12:]
    fle.close()
    size = len(lst)
    imp_date_end = lst[1].split(';')[2]
    imp_date_start = lst[size - 1].split(';')[2]
    exp_dates = pd.date_range(start=imp_date_start, end=imp_date_end)
    imp_date_lst = list()
    imp_p_lst = list()
    for i in range(size - 1, 0, -1):
        def_row = lst[i].split(';')
        # print('Id: {}'.format(i), end='\t')
        # print(def_row[13:45])
        lcl_date = def_row[2]
        lcl_month = lcl_date[2:]
        for j in range(0, 31):
            lcl_p_str = def_row[13:44][j]
            if lcl_p_str == '':
                lcl_p_int = 0
            else:
                lcl_p_int = float(stringsf.convert_dec_sep(lcl_p_str))
            if j < 9:
                lcl_day = '0' + str(j + 1)
            else:
                lcl_day = str(j + 1)
            lcl_date_full = lcl_day + lcl_month
            imp_date_lst.append(lcl_date_full)
            imp_p_lst.append(lcl_p_int)

    exp_p_lst = list()
    exp_dates_lst = list()
    count = 0
    recount = 0
    for i in range(0, len(exp_dates)):
        lcl_date_str = stringsf.codify_int(exp_dates[i].day) + '/' + stringsf.codify_int(exp_dates[i].month) + '/' \
                       + str(exp_dates[i].year)
        exp_dates_lst.append(lcl_date_str)
        while True:
            # print('Searching for {}\tLocal date: {}'.format(lcl_date_str, imp_date_lst[count - 1]))
            if lcl_date_str == imp_date_lst[count]:
                exp_p_lst.append(imp_p_lst[count])
                # print('OK\tFound')
                recount = count
                break
            elif int(lcl_date_str.split('/')[2]) < int(imp_date_lst[count].split('/')[2]):  # not found
                exp_p_lst.append(0.0)
                count = recount + 1
                # print('Not found')
                break
            count = count + 1

    df = pd.DataFrame({'Date': exp_dates_lst, 'P (mm)': exp_p_lst})
    out_file = p0.split('.')[0] + '_processed.txt'
    df.to_csv(out_file, sep=';', index=False)
    return df


def txt_to_list(p0='txt_data', p1=';', p2=1, p3=-999, p4=False, p5=5, p6=True, p7='utf-8'):
    """
    load a .txt file to a nth-D list
    :param p0: data file name - without extension
    :param p1: separator string
    :param p2: line index to start loading data (first line is 0)
    :param p3: error value
    :param p4: bool to enter slicing mode (i.e. to load only some lines of data)
    :param p5: line index to stop (inclusive) loading data (first line is 0)
    :param p6: bool control to float format conversion. Else the data returns as string format.
    :param p7: open parameter for encoding
    :return: nth-D list with float data or string format
    """
    c = 0  # set counter
    flenm = p0 + '.txt'
    fle = open(flenm, 'r', encoding=p7)  # open file in reading mode
    # go to starting line:
    for i in range(0, p2):
        fle.readline()  # skip head lines
        c = c + 1
    str_lst = list()
    # append string lines to aux list
    if p4:  # conditional to enter slicing mode
        # if p5 == p4:
        # p5 = p4 + 1
        c = 0
        while True:
            line = fle.readline()
            n = len(line) - 1  # getting rid of '\n' at the end of each line
            str_lst.append(str(line[:n]))
            c = c + 1
            if c == p5:
                break
    else:  # regular protocol
        for line in fle:
            n = len(line) - 1  # getting rid of '\n' at the end of each line
            str_lst.append(str(line[:n]))
    str_nd_lst = list()
    # split string lines by separator
    for lines in str_lst:
        str_row = lines.split(p1)
        str_nd_lst.append(str_row[:])
    str_lst.clear()
    if p6:
        # convert string formats to float:
        flt_row = list()
        flt_mtx = list()
        for i in range(0, len(str_nd_lst)):
            for j in range(0, len(str_nd_lst[i])):
                try:
                    flt_row.append(float(str_nd_lst[i][j]))
                except ValueError:
                    flt_row.append(p3)
            flt_mtx.append(flt_row[:])
            flt_row.clear()
        # print(m2)  # >> check point
        fle.close()
        str_nd_lst.clear()  # cleaning the string list
        return flt_mtx
    else:
        return str_nd_lst


def txt_to_str_list(p0='txt_data', p2=1, p4=False, p5=5):
    """
    load a .txt file lines in string format to a nth-D list
    :param p0: data file name
    :param p2: line index to start loading data (first line is 0)
    :param p4: bool to enter slicing mode (i.e. to load only some lines of data)
    :param p5: line index to stop (inclusive) loading data (first line is 0)
    :return: nth-D list with the lines of .txt file
    """
    c = 0  # set counter
    fleNm = p0 + '.txt'
    fle = open(fleNm, 'r')  # open file in reading mode
    # go to starting line:
    for i in range(0, p2):
        fle.readline()  # skip head lines
        c = c + 1
    str_lst = list()
    # append string lines to aux list
    if p4:  # conditional to enter slicing mode
        if p5 == p4:
            p5 = p4 + 1
        while True:
            line = fle.readline()
            n = len(line) - 1  # getting rid of '\n' at the end of each line
            str_lst.append(str(line[:n]))
            c = c + 1
            if c == p5:
                break
    else:  # regular protocol
        for line in fle:
            n = len(line) - 1  # getting rid of '\n' at the end of each line
            str_lst.append(str(line[:n]))
    return str_lst


def load_nline2str(p0, p1):
    def_flenm = p0
    def_fle = open(def_flenm, 'r')  # open file in reading mode
    # skip all necessary lines:
    def_k = 0
    while def_k < p1 - 1:
        def_fle.readline()
        def_k = def_k + 1
    # load n-th line to object
    def_line = def_fle.readline()
    return str(def_line)


def load_nline2list(p0, p1, p2=';', p3=True):
    """
    extract n-th line to a list object
    :param p0: file path
    :param p1: n-th line (first line is 1)
    :param p2: separator
    :param p3: boolean to load convertible values to float
    :return: list object
    """
    def_flenm = p0
    def_fle = open(def_flenm, 'r')  # open file in reading mode
    # skip all necessary lines:
    def_k = 0
    while def_k < p1 - 1:
        def_fle.readline()
        def_k = def_k + 1
    # load n-th line to object
    def_line = def_fle.readline()
    # cut off '\n' at the end:
    def_n = len(str(def_line)) - 2
    def_line = def_line[:def_n]
    def_line = def_line.split(p2)
    if p3:
        def_aux_lst = list()
        for def_e in def_line:
            try:
                def_e = float(def_e)
            except ValueError:
                pass
            def_aux_lst.append(def_e)
        def_line = def_aux_lst
    return def_line


def filename_dialog(p0="txt", p1=".txt file", p2="select file", p3=False):
    """
    this function displays a dialog and returns a file name (full path)
    :param p0: file extension without the dot
    :param p1: file type string
    :param p2: title string
    :return: string with file name (full path)
    """
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
    while True:
        root = Tk()
        root.withdraw()
        def_aux_str = "*." + p0
        def_filename = askopenfilename(initialdir="/", title=p2, filetypes=((p1, def_aux_str), ("all files", "*.*")))
        root.destroy()
        def_filename = str(def_filename)
        if def_filename.split('.')[-1] == p0:
            if p3:
                def_aux_str = 'chosen file: ' + def_filename
                display.okinput(p0=def_aux_str)
            break
        else:
            if p3:
                def_aux_str = 'Invalid file type: must be .' + p0
                display.errorinput(p0=def_aux_str)
    return def_filename


def demo():
    var = filename_dialog()
    print(var)

# demo()

"""
lst = txt_to_list('/users/ipo/desktop/data', p2=3, p4=True, p5=9)
for i in range(0, len(lst)):
    print(i, end=' >>> ')
    print(lst[i])
"""
