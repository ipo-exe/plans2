# some tools

import numpy as np
from scipy import stats


def list_ixj_to_jxi(p0):
    """
    a function designed to take a 2d list with i x j relation
    and convert to a 2d list  j x i
    :param p0:
    :return: a new list
    """
    lst = list()
    # loop across new lines
    for i in range(0, len(p0[0])):
        r = list()
        # loop across new columns
        for j in range(0, len(p0)):
            aux_flt = p0[j][i]
            r.append(aux_flt)
        lst.append(r[:])
        r.clear()
    return lst


def scoreofpercentiles(p0):
    def_a = p0
    def_sop = list()
    for def_i in range(0, np.size(def_a)):
        def_lcl_pos = stats.percentileofscore(def_a, def_a[def_i], kind='weak')
        def_sop.append(def_lcl_pos)
    def_sop = np.array(def_sop)
    return def_sop

'''
clr = True
test = save.create_new_txt_file('teste')
rlt = [[0, 4, 5], [6, 66, 666]]
print(rlt)
lst = list_ixj_to_jxi(rlt)
print(lst)
lbls = ['label 1', 'label 2']
display.rlt_2d_float(lst, lbls, p10=False, clr=clr)
save.append_2d_frlt(test, lst, lbls)
'''