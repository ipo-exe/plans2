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
#               this program contains a set of custom functions for validation of input data


from tools import color, display


def integer(p0='Enter integer input: ', clr=False):
    """
    validate an integer number input
    :param p0: string instruction
    :param clr: color boolean control
    :return: the entered integer number
    """
    while True:  # runs the loop until the input is valid
        while True:  # internal loop for null input
            v_vldt = input(p0).strip()
            if v_vldt != '':
                break
        try:
            v_vldt = int(v_vldt)  # try to convert to integer
            display.okinput(clr=clr)
            break
        except ValueError:
            display.errorinput(clr=clr)
    return v_vldt


def integer_positive(p0='Enter positive integer input: ', clr=False):
    """
    validate integer positive input
    :param p0: string instruction
    :param clr: color boolean control
    :return: integer positive number
    """
    while True:
        while True:
            v_vldt = input(p0).strip()
            if v_vldt != '':
                break
        try:
            v_vldt = int(v_vldt)
            if v_vldt >= 0:
                display.okinput(clr=clr)
                break
            else:
                display.errorinput(clr=clr)
        except ValueError:
            display.errorinput(clr=clr)
    return v_vldt


def integer_negative(p0='Enter negative integer input: ', clr=False):
    """
    validate integer positive input
    :param p0: string instruction
    :param clr: color boolean control
    :return: integer negative number
    """
    while True:
        while True:
            v_vldt = input(p0).strip()
            if v_vldt != '':
                break
        try:
            v_vldt = int(v_vldt)
            if v_vldt < 0:
                display.okinput(clr=clr)
                break
            else:
                display.errorinput(clr=clr)
        except ValueError:
            display.errorinput(clr=clr)
    return v_vldt


def integer_hithan(p0=0, p1='Enter integer input higher than', clr=False):
    """
    validate integer higher than given number (exclusive)
    :param p0: given number to be higher
    :param p1: string instruction
    :param clr: color boolean control
    :return: integer input
    """
    while True:
        while True:
            v_vldt = input('{} {}: '.format(p1, p0)).strip()
            if v_vldt != '':
                break
        try:
            v_vldt = int(v_vldt)
            if v_vldt > p0:
                display.okinput(clr=clr)
                break
            else:
                display.errorinput(clr=clr)
        except ValueError:
            display.errorinput(clr=clr)
    return v_vldt


def integer_lothan(p0=0, p1='Enter integer input lower than', clr=False):
    """
    validate integer lower than given number (exclusive)
    :param p0: given number to be lower
    :param p1: string instruction
    :param clr: color boolean control
    :return: integer input
    """
    while True:
        while True:
            v_vldt = input('{} {}: '.format(p1, p0)).strip()
            if v_vldt != '':
                break
        try:
            v_vldt = int(v_vldt)
            if v_vldt < p0:
                display.okinput(clr=clr)
                break
            else:
                display.errorinput(clr=clr)
        except ValueError:
            display.errorinput(clr=clr)
    return v_vldt


def integer_positive_lothan(p0=100, p1='Enter positive integer input lower than', clr=False):
    """
    validate positive integer but lower than given number (exclusive)
    :param p0: given number to be lower
    :param p1: string instruction
    :param clr: color boolean control
    :return: integer input
    """
    while True:
        while True:
            v_vldt = input('{} {}: '.format(p1, p0)).strip()
            if v_vldt != '':
                break
        try:
            v_vldt = int(v_vldt)
            if 0 <= v_vldt < p0:
                display.okinput(clr=clr)
                break
            else:
                display.errorinput(clr=clr)
        except ValueError:
            display.errorinput(clr=clr)
    return v_vldt


def integer_rng(p0=0, p1=100, p2='Enter integer input between the range ', clr=False):
    """
    validate integer between given range (inclusive)
    :param p0: lower limit
    :param p1: higher limit
    :param p2: string instruction
    :param clr: color boolean control
    :return: integer input
    """
    while True:
        while True:
            v_vldt = input('{} [{} - {}]: '.format(p2, p0, p1)).strip()
            if v_vldt != '':
                break
        try:
            v_vldt = int(v_vldt)
            if p0 <= v_vldt <= p1:
                display.okinput(clr=clr)
                break
            else:
                display.errorinput(clr=clr)
        except ValueError:
            display.errorinput(clr=clr)
    return v_vldt


def flt(p0='Enter float input: ', clr=False):
    """
    validate float input
    :param p0: string instruction
    :param clr: color boolean control
    :return: float input
    """
    while True:
        while True:
            v_vldt = input(p0).strip()
            if v_vldt != '':
                break
        try:
            display.okinput(clr=clr)
            v_vldt = float(v_vldt)
            break
        except ValueError:
            display.errorinput(clr=clr)
    return v_vldt


def positive_flt(p0='Enter positive float input: ', clr=False):
    """
    validate positive float input
    :param p0: string instruction
    :param clr: color boolean control
    :return: float input
    """
    while True:
        while True:
            v_vldt = input(p0).strip()
            if v_vldt != '':
                break
        try:
            v_vldt = float(v_vldt)
            if v_vldt >= 0:
                display.okinput(clr=clr)
                break
            else:
                display.errorinput(clr=clr)
        except ValueError:
            display.errorinput(clr=clr)
    return v_vldt


def flt_pstv_lothan(p0=100, p1='Enter positive float input lower than', clr=False):
    """
    validate positive float but lower than given number (exclusive)
    :param p0: given number to be lower
    :param p1: string instruction
    :param clr: color boolean control
    :return: float input
    """
    while True:
        while True:
            v_vldt = input('{} {}: '.format(p1, p0)).strip()
            if v_vldt != '':
                break
        try:
            v_vldt = float(v_vldt)
            if 0 <= v_vldt < p0:
                display.okinput(clr=clr)
                break
            else:
                display.errorinput(clr=clr)
        except ValueError:
            display.errorinput(clr=clr)
    return v_vldt


def flt_hithan(p0=0, p1='Enter float input higher than', clr=False):
    """
    validate float input but higher than given number
    :param p0: number to be higher
    :param p1: string instruction
    :param clr: color boolean control
    :return: float input
    """
    while True:
        while True:
            v_vldt = input('{} {}: '.format(p1, p0)).strip()
            if v_vldt != '':
                break
        try:
            v_vldt = float(v_vldt)
            if v_vldt > p0:
                display.okinput(clr=clr)
                break
            else:
                display.errorinput(clr=clr)
        except ValueError:
            display.errorinput(clr=clr)
    return v_vldt


def negative_float(p0='Enter negative float input: ', clr=False):
    """
    validate negative float input
    :param p0: string instruction
    :param clr: color boolean control
    :return: float input
    """
    while True:
        while True:
            v_vldt = input(p0).strip()
            if v_vldt != '':
                break
        try:
            v_vldt = float(v_vldt)
            if v_vldt < 0:
                display.okinput(clr=clr)
                break
            else:
                display.errorinput(clr=clr)
        except ValueError:
            display.errorinput(clr=clr)
    return v_vldt


def string_ans(p0=2, p1='yn', p2='Do you want to continue? ', clr=False):
    """
    validate string input for answer question
    :param p0: number of possible answers
    :param p1: string of concatenated answer keys
    :param p2: string question
    :param clr: color boolean control
    :return: string input
    """
    if len(p1) > p0:
        p0 = len(p1)
    while True:
        aux_s = ''
        for i in range(0, p0):
            if i < p0 - 1:
                aux_s = aux_s + p1[i].upper() + '/'
            else:
                aux_s = aux_s + p1[i].upper()
        while True:
            if clr:
                vs_vldt = input('\n>>> ' + p2 + color.bldcyan(' [' + aux_s + '] '))
            else:
                vs_vldt = input('\n>>> ' + p2 + ' [' + aux_s + '] ')
            if vs_vldt != '':
                vs_vldt = vs_vldt.strip().upper()[0]
                break
        if vs_vldt in p1.upper():
            display.okinput(clr=clr)
            break
        display.errorinput(clr=clr)
    return vs_vldt


def string_menu(p0, p1='Options keys', p2='Enter menu key: ', p3='You chose: ',
                p4=False, p5='e', p6='exit menu', clr=False):
    """
    validade menu
    :param p0: list with menu keys
    :param p1: menu header
    :param p2: string instruction
    :param p3: string feedback
    :param p4: boolean to control exception key mode
    :param p5: exception key string
    :param p6: exception key feedback message
    :param clr: color boolean control
    :return:
    """
    # built list for summary display:
    def_aux_lst1 = list()
    def_aux_str = '\n>>> ' + p2
    for def_i in range(0, len(p0)):
        def_aux_lst2 = [' ' + str(p0[def_i]), def_i]
        def_aux_lst1.append(def_aux_lst2[:])
        def_aux_lst2.clear()
    # display menu:
    display.summary(def_aux_lst1, p1=p1, p2=0, clr=clr)
    # if exception key:
    if p4:
        # validation loop:
        while True:
            # loop to keep asking for full entry:
            while True:
                def_key = input(def_aux_str).strip()
                if def_key != '':
                    break
            # in case of exception key
            if def_key == p5:
                def_option = def_key
                print('>>> {} {}'.format(p3, p6))
                display.okinput(clr=clr)
                break
            else:  # validate the entry
                try:
                    def_key = int(def_key)
                    if def_key >= 0:
                        display.okinput(clr=clr)
                        def_option = def_aux_lst1[def_key][0].strip()
                        print('>>> {} {}'.format(p3, def_option))
                        display.okinput(clr=clr)
                        break
                    else:
                        display.errorinput(clr=clr)
                except ValueError:
                    display.errorinput(clr=clr)
    else:
        # validation loop:
        while True:
            def_key = integer_positive(p0=def_aux_str, clr=clr)
            if def_key < len(p0):
                break
            else:
                display.errorinput(clr=clr)
        def_option = def_aux_lst1[def_key][0].strip()
        print('{} {}'.format(p3, def_option))
        display.okinput(clr=clr)
    return def_option


def string_alnum(p0=15, p1='Enter name: ', clr=False):
    """
    validation of string with max lenght and just alnum chars
    :param p0: max length
    :param p1: instruction string
    :param clr: color boolean control
    :return: string
    """
    print('[max of {} chars and no special chars (including whitespace)]'.format(p0))
    while True:
        def_str = input(p1).strip().lower()
        # length validation:
        if len(def_str) > p0:
            display.errorinput(p0='string too long!', clr=clr)
        else:  # chars validation
            def_aux_int = 0
            for def_c in def_str:
                if def_c.isalnum():
                    def_aux_int = def_aux_int + 0
                else:
                    def_aux_int = def_aux_int + 1
            if def_aux_int == 0:  # no special chars
                display.okinput(clr=clr)
                break
            else:
                def_aux_str = str(def_aux_int) + ' special characters found'
                display.errorinput(p0=def_aux_str)
    return def_str


def string_filename(p0=15, p1='Enter name: ', p2='string too long! max of', p3='special characters found', clr=False):
    """
    validation of string with max lenght and just file name valid chars
    :param p0: max length
    :param p1: instruction string
    :param p2: warning instruction 1
    :param p3: warning instruction 2
    :param clr: color boolean control
    :return: string
    """
    while True:
        def_str = input(p1).strip().lower()
        # length validation:
        if len(def_str) > p0:
            def_aux_str = p2 + ': ' + str(p0)
            display.errorinput(p0=def_aux_str, clr=clr)
        else:  # chars validation
            def_aux_int = 0
            for def_c in def_str:
                if def_c.isalnum() or def_c == '_':
                    def_aux_int = def_aux_int + 0
                else:
                    def_aux_int = def_aux_int + 1
            if def_aux_int == 0:  # no special chars
                display.okinput(clr=clr)
                break
            else:
                def_aux_str = str(def_aux_int) + ' ' + p3
                display.errorinput(p0=def_aux_str)
    return def_str


def string_lowlen(p0=100, p1='Enter text: ', clr=False):
    """
    validation of string with len lower than a fixed number
    :param p0: max length
    :param p1: string instruction
    :param clr: color boolean control
    :return: string
    """
    print('[max of {} characters]'.format(p0))
    while True:
        def_str = input(p1).strip().lower()
        # length validation:
        if len(def_str) > p0:
            display.errorinput(p0='string too long!', clr=clr)
        else:
            break
    return def_str


def permission_protocol(p0='Are you ready?', p1='Ok. We can wait.', p2=0.5):
    # loading permission protocol
    while True:
        lcl_aux_str = string_ans(p2=p0)
        if lcl_aux_str == 'Y':
            break
        else:
            display.waiting(p1=p1, p2=p2)


def demo():
    def_list = ['option1', 'option2', 'option3']
    def_msg = 'Enter menu key [ <e> to exit]:'
    def_option = string_menu(def_list, p2=def_msg, p4=True)


# demo()
