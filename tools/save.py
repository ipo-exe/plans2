# saving data and log files to hard drive
from tools import stringsf, display, validate
import os


def create_new_dir(p0='new_directory', p1=False, p2=False, clr=False):
    """
    create new directory. If the dir already exists, then verify if is empty. If is not empty, creates a new version
    :param p0: new dir path
    :param p1: user interaction boolean control
    :param p2: print boolean control
    :param clr: color boolean control
    :return: dir path string
    """
    def_nm = p0
    if os.path.exists(def_nm):  # dir exists
        if len(os.listdir(def_nm)) == 0:  # dir is empty so whatever
            if p2:
                def_aux_str = 'empty directory found at: ' + def_nm
                display.okinput(p0=def_aux_str, clr=clr)
        else:  # dir is not empty
            def_aux_str = def_nm + ' directory already exists!'
            display.wrnginput(p0=def_aux_str, clr=clr)
            if p1:  # enter user interaction
                while True:
                    def_nm_entry = validate.string_alnum(p1='Rename directory:', clr=clr)
                    def_nm = '/'.join(p0.split('/')[:-1]) + '/' + def_nm_entry
                    print(def_nm)
                    if os.path.exists(def_nm):
                        def_aux_str = 'directory already exists!'
                        display.wrnginput(p0=def_aux_str, clr=clr)
                    else:
                        os.mkdir(def_nm)
                        def_aux_str = 'directory created at: ' + def_nm
                        display.okinput(p0=def_aux_str, clr=clr)
                        break
            else:  # skip user interaction and give a new name
                k = 0
                while True:  # loop to find the new name
                    k = k + 1
                    def_nm = p0 + '_v' + str(k)  # build new name
                    try:
                        os.mkdir(def_nm)
                        def_aux_str = p0 + 'directory renamed to: ' + def_nm
                        display.wrnginput(p0=def_aux_str, clr=clr)
                        display.okinput(clr=clr)
                        break  # go out of loop
                    except FileExistsError:
                        pass  # stay in loop
    else:  # dir not exists
        os.mkdir(def_nm)
        if p2:
            def_aux_str = 'directory created at: ' + def_nm
            display.okinput(p0=def_aux_str, clr=clr)
    return def_nm


def create_new_txt_file(p0='new_file'):
    """
    creates a new .txt file and append '' to it.
    :param p0: file name without extension
    :return: file name string with extension
    """
    flenm = p0 + '.txt'
    fle = open(flenm, 'w+')
    fle.write('')
    fle.close()
    return flenm


def create_new_file(p0='new_file', p1='.txt'):
    """
    creates a new file and append '' to it.
    :param p0: file name without extension
    :param p1: file string extension
    :return: file name string with extension
    """
    flenm = p0 + p1
    fle = open(flenm, 'w+')
    fle.write('')
    fle.close()
    return flenm


def copy_txt_file(p0, p1, p2='copied'):
    """
    copy a txt file
    :param p0: input string file path with extension .txt
    :param p1: output diretory string path
    :param p2: output file name without extension
    :return: file name string with extension
    """
    def_in = open(p0, 'r')
    def_lst = def_in.readlines()
    def_in.close()
    def_aux_str = p1 + '/' + p2
    def_out_nm = create_new_file(def_aux_str)
    def_out = open(def_out_nm, 'r+')
    def_out.writelines(def_lst)
    def_out.close()
    def_aux_str = 'file copied to: ' + str(def_out_nm)
    display.okinput(p0=def_aux_str, p1=0.1)
    return def_out_nm


def copy_file(p0, p1, p2='copied.txt', p3=False):
    """
    copy a file
    :param p0: input string file path with extension
    :param p1: output diretory string path
    :param p2: output file name with extension
    :param p3: print boolean control
    :return: file name string with extension
    """
    def_in = open(p0, 'r')
    def_lst = def_in.readlines()
    def_in.close()
    def_fle_nm = p2.split('.')[0]
    def_fle_ext = '.' + p2.split('.')[1]
    def_aux_str = p1 + '/' + def_fle_nm
    def_out_nm = create_new_file(def_aux_str, p1=def_fle_ext)
    def_out = open(def_out_nm, 'r+')
    def_out.writelines(def_lst)
    def_out.close()
    if p3:
        def_aux_str = 'file copied to: ' + str(def_out_nm)
        display.okinput(p0=def_aux_str, p1=0.1)
    return def_out_nm


def createreport(p0='Run_Report'):
    flmtime = stringsf.nowsep()
    flenm = p0 + '_' + flmtime + '.txt'
    fle = open(flenm, 'w+')
    fle.write('timestamp: ' + flmtime + '\n')
    fle.close()
    return flenm


def appendtitle(p0, p1='title'):
    fle = open(p0, 'a+')
    fle.write(stringsf.title(p1) + '\n')
    fle.close()


def appendsubtitle(p0, p1='subtitle'):
    fle = open(p0, 'a+')
    fle.write(stringsf.subtitle(p1) + '\n')
    fle.close()


def appendtext(p0, p1='text', p2='\n'):
    """
    append text to .txt file
    :param p0: file name (path and extension)
    :param p1: text string to append
    :param p2: text string to end text
    :return: none
    """
    fle = open(p0, 'a+')
    fle.write(p1 + p2)
    fle.close()


def edit_line(p0, p1, p2='new text'):
    """
    edit line in .txt file
    :param p0: file name (path and extension - it must be .txt)
    :param p1: edit line index (first line is 0)
    :param p2: text to apppend
    :return: none
    """
    def_fle = open(p0, 'r+')  # read and write mode. starts at the begining of file
    def_lines = def_fle.readlines()  # load all lines to list
    def_lines[p1] = p2 + '\n'  # change tx  he desired line in list
    def_fle.close()  # close
    def_fle = open(p0, 'w')  # open again just to overwrite
    def_fle.writelines(def_lines)  # overwrite the file
    def_fle.close()


def edit_lines(p0, p1, p2):
    """
    edit line block in .txt file
    :param p0: file name (path and extension - it must be .txt)
    :param p1: first line index in block (first line in file is 0)
    :param p2: list with lines strings. Strings must NOT end with '\n'.
    :return: none
    """
    def_counter = p1
    for def_line in p2:
        edit_line(p0, def_counter, def_line)
        def_counter = def_counter + 1


def append_2d_csv(p0, p1, p2=';'):
    """
    save to file comma separated values
    :param p0: file name with extension
    :param p1: list
    :param p2: separator
    :return: none
    """
    fle = open(p0, 'a+')
    for i in range(0, len(p1)):
        def_aux_str = ''
        for j in range(0, len(p1[i])):
            def_aux_str = def_aux_str + str(p1[i][j]) + p2
        fle.write(def_aux_str + '\n')
    fle.close()


def append_1d_fmatrix(flenm, p0, p1='Field', p2='Elements', p3=1, p4='Title', p5=True):
    fle = open(flenm, 'a+')
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
        # writing upper line
        fle.write('_' * c)
        fle.write('\n')
        # writing header
        fle.write(stringsf.center(p4.upper(), c))
        fle.write('\n')
        fle.write(' ' * a)
        for i in range(0, len(p0)):
            s = p1 + ' ' + str(int(i))
            if p5:
                s = p1 + ' ' + str(int(i + 1))
            fle.write(stringsf.center(s, b))
        fle.write('\n')
        break
    # elements:
    while True:
        fle.write(stringsf.center(p2, p1=a))
        for i in range(0, len(p0)):
            fle.write(stringsf.center(str(round(p0[i], p3)), p1=b))
        fle.write('\n')
        break
    fle.write('_' * c)
    fle.write('\n')
    fle.close()


def append_2d_fmatrix(flenm, p0, p1='Fld', p2='Rcrd', p3=1, p4='Flds', p5='Records',
                      p6=1.0, p7=0.0, p8=True, p9='Title', p12=0):
    """
    This function writes a matrix of float numbers in a fancy way into a .txt file
    :param flenm: .txt file name
    :param p0: 2D list containing matrix
    :param p1: minor label for columns
    :param p2: minor label for lines
    :param p3: decimal plates of float numbers
    :param p4: major label for columns
    :param p5: major label for lines
    :param p6: A parameter for linear index transformation
    :param p7: B parameter for linear index transformation
    :param p8: boolean to set index starting in 1 (True) or 0 (False)
    :param p9: title of matrix
    :param p12: decimal plates for labels
    :return: no return
    """
    fle = open(flenm, 'a+')
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
    # write header:
    while True:
        # writing upper line:
        fle.write('_' * c)
        fle.write('\n')
        # writing title:
        fle.write(stringsf.center(p9.upper(), c))
        fle.write('\n')
        # writing upper header:
        aux_s2 = stringsf.center(p5, a)
        aux_s3 = stringsf.center(p4, (c - a))
        aux_s4 = aux_s2 + aux_s3
        fle.write(aux_s4)
        fle.write('\n')
        # writing sub header
        fle.write(' ' * a)
        for i in range(0, len(p0[0])):
            if p8:
                aux_i3 = i + 1
            else:
                aux_i3 = i
            aux_f1 = (aux_i3 * p6) + p7  # linear transformation on label
            aux_s4 = p1 + ' ' + str(round(aux_f1, p12))
            if p12 == 0:
                aux_s4 = p1 + ' ' + str(int(aux_f1))
            fle.write(stringsf.center(aux_s4, b))
            # print(color.bldwhite(string.center(aux_s4, b)), end='')
        fle.write('\n')
        # print()
        break
    # writing elements:
    while True:
        for i in range(0, len(p0)):
            if p8:
                aux_i3 = i + 1
            else:
                aux_i3 = i
            aux_f1 = (aux_i3 * p6) + p7  # linear transformation on label
            aux_s4 = p2 + ' ' + str(round(aux_f1, p12))
            if p12 == 0:
                aux_s4 = p2 + ' ' + str(int(aux_f1))
            fle.write(stringsf.center(aux_s4, a))
            # print(color.bldwhite(string.center(aux_s4, a)), end='')
            for j in range(0, len(p0[i])):
                fle.write(stringsf.center(str(round(p0[i][j], p3)), b))
                # print(color.bldgreen(string.center(str(round(p0[i][j], p3)), b)), end='')
            fle.write('\n')
            # print()
        break
    # final line:
    fle.write('_' * c)
    fle.write('\n')
    fle.close()


def append_2d_frlt(flenm, p0, p1, p2='Rcrd', p3=1, p5='Records',
                   p6=1.0, p7=0, p8=True, p9='Title', p12=0):
    """
    This function writes on file a 2D relation of float numbers in a fancy way
    Therefore it must receive a list of header labels (p1)
    Parameter p4 does not exist here.
    :param flenm: .txt file name
    :param p0: 2D list containing matrix
    :param p1: list of minor labels for columns
    :param p2: minor label for lines
    :param p3: decimal plates of float numbers
    :param p5: major label for lines
    :param p6: A parameter for linear index transformation
    :param p7: B parameter for linear index transformation
    :param p8: boolean to set index starting in 1 (True) or 0 (False)
    :param p9: title of matrix
    :param p12: decimal plates for labels
    :return: no return
    """
    fle = open(flenm, 'a+')
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
        fle.write('_' * c)
        fle.write('\n')
        # printing title:
        fle.write(stringsf.center(p9.upper(), c))
        fle.write('\n')
        # printing header:
        aux_s2 = stringsf.center(p5, a)
        fle.write(aux_s2)
        for i in range(0, len(p1)):
            aux_s4 = p1[i]
            fle.write(stringsf.center(aux_s4, b))
        fle.write('\n')
        break
    # elements:
    while True:
        for i in range(0, len(p0)):
            if p8:
                aux_i3 = i + 1
            else:
                aux_i3 = i
            aux_i4 = (aux_i3 * p6) + p7  # linear transformation on label
            aux_s4 = p2 + ' ' + str(round(aux_i4, p12))
            if p12 == 0:
                aux_s4 = p2 + ' ' + str(int(aux_i4))
            fle.write(stringsf.center(aux_s4, a))
            for j in range(0, len(p1)):
                fle.write(stringsf.center(str(round(p0[i][j], p3)), p1=b))
            fle.write('\n')
        break
    # final line:
    fle.write('_' * c)
    fle.write('\n')
    fle.close()


def append_summary(flenm, p0, p1='summary', p2=1):
    """
    function designed to save to .txt a data summary
    :param flenm: file name
    :param p0: 2D list with labels and values
    :param p1: title
    :param p2: decimal plates
    :return: none
    """
    fle = open(flenm, 'a+')
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
        break
    # print header
    fle.write('_' * c)
    fle.write('\n')
    fle.write(stringsf.center(p0=p1, p1=c).upper())
    fle.write('\n')
    # print elements
    for i in range(0, len(p0)):
        aux_s1 = str(p0[i][0]).lower().capitalize()
        d = c - len(aux_s1) - b
        aux_s2 = '.' * d
        aux_s3 = str(round(p0[i][1], p2))
        aux_s4 = aux_s1 + aux_s2 + aux_s3
        fle.write(aux_s4)
        fle.write('\n')
    fle.write('_' * c)
    fle.write('\n')
    fle.close()


def append_time_series(flenm, p0, p1, p2, p3='time series'):
    """
    function designed to save to file a time series relationship
    :param flenm: txt file name
    :param p0: 2d list containing data
    :param p1: 1d list of head labels
    :param p2: 1d list of series resolution
    :param p3: title
    :return:
    """
    fle = open(flenm, 'a+')
    # get sizing parameters
    c = 0
    for e in p1:
        c = c + len(str(e)) + 2
    # print header:
    fle.write('_' * c)
    fle.write('\n')
    aux_str = stringsf.center(p0=p3, p1=c).upper()
    fle.write(aux_str)
    fle.write('\n')
    # print head labels
    for e in p1:
        aux_str = ' ' + str(e) + ' '
        fle.write(aux_str)
    fle.write('\n')
    # print elements
    for i in range(0, len(p0)):
        for j in range(0, len(p0[i])):
            aux_int = len(str(p1[j])) + 2
            aux_str = stringsf.center(str(round(p0[i][j], p2[j])), p1=aux_int)
            fle.write(aux_str)
        fle.write('\n')
    fle.write('\n')
    fle.close()


def delete_dir(p0):
    if os.path.exists(p0):  # dir exists
        if len(os.listdir(p0)) == 0:  # dir is empty
            os.rmdir(p0)
        else:
            clear_dir(p0)
            os.rmdir(p0)
    else:
        pass


def clear_dir(p0):
    def_lst = os.listdir(p0)
    if len(def_lst) == 0:  # dir is empty
        pass
    else:
        for def_elem in def_lst:
            def_fle_pth = p0 + '/' + def_elem
            os.remove(def_fle_pth)



def demo():
    f = create_new_txt_file('newfile')
    text = 'okgo go go go '
    appendtext(f, text)
    appendtext(f, text)
    appendtext(f, text)
    appendtext(f, text)
    appendtext(f, text)
    appendtext(f, text)
    edit_line(f, 1)
    aux_lst = ['shit1', 'shit2']
    edit_lines(f, 2, aux_lst)


#demo()

# dir = create_new_dir('newdir', p1=True)

'''
now = datetime.datetime.now()
print(now)
year = now.strftime('%Y')
print(year)
print(type(year))
print(type(now))

m = [[0, 2, 4, 5, 6, 7], [0, 2, 5, 7, 3, 666]]
nm = createreport()
appendtitle(nm, 'move bitch')
appendsubtitle(nm, 'g-unit in the house')
append_2d_fmatrix(nm, m)
append_1d_fmatrix(nm, m[0])

'''
