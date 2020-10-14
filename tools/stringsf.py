# some useful strings for printing :)
import datetime


def title(p0='title', p1=70, p2='*', p3=True):
    """
    Returns a title string like:


    ********************** TITLE **********************


    :param p0: body of text
    :param p1: size of title
    :param p2: character of decorations
    :param p3: spaces boolean
    :return: a string
    """
    if len(p0) > p1:
        title_aux0 = ''
    else:
        title_aux0 = str(p2 * int((p1 - (len(p0))) / 2))
    title_s = title_aux0 + ' ' + p0.upper() + ' ' + title_aux0
    if p3:
        title_s = '\n\n\n' + title_s + '\n\n'
    return title_s


def subtitle(p0='subtitle', p1=60, p2='*', p3=True):
    """
    Returns a subtitle string like:

        ********** Subtitle

    :param p0: body of text
    :param p1: size of subtitle
    :param p2: character of decorations
    :param p3: space boolean
    :return: a string
    """
    if len(p0) > p1:
        subtitle_aux0 = ''
    else:
        subtitle_aux0 = str(p2 * int((p1 - (len(p0))) / 2))
    subtitle_s = subtitle_aux0 + ' ' + p0.capitalize() + ' ' + subtitle_aux0
    if p3:
        subtitle_s = '\n' + subtitle_s + '\n'
    return subtitle_s


def center(p0='text', p1=8):
    """
    return a centered string
    :param p0: text to centralize
    :param p1: full length to center
    :return: centered string
    """
    if len(p0) > p1:  # in case the text is longer than the length param
        s = ' ' + p0 + ' '
    else:
        # symmetry:
        if (p1 - len(p0)) % 2 == 0:
            aux_i1 = int((p1 - len(p0))/2)
            s = (' '*aux_i1) + p0 + (' '*aux_i1)
        #
        else:
            aux_i1 = int(round((p1 - len(p0))/2))
            aux_i2 = int((p1 - len(p0)) - aux_i1)
            s = (' '*aux_i2) + p0 + (' '*aux_i1)
    return s


def nowsep(p0='-'):
    def_now = datetime.datetime.now()
    yr = def_now.strftime('%Y')
    mth = def_now.strftime('%m')
    dy = def_now.strftime('%d')
    hr = def_now.strftime('%H')
    mn = def_now.strftime('%M')
    sg = def_now.strftime('%S')
    def_lst = [yr, mth, dy, hr, mn, sg]
    def_s = str(p0.join(def_lst))
    return def_s


def now():
    s = str(datetime.datetime.now())
    return s


def merge_sep(p0, p1=';'):
    def_aux_str1 = ''
    for i in range(0, len(p0)):
        def_aux_str1 = def_aux_str1 + str(p0[i]) + p1
    return def_aux_str1


def convert_dec_sep(p0, p1=True):
    def_old_str = p0
    if p1:
        try:
            new = float(def_old_str)
        except ValueError:
            def_hi = def_old_str.split(',')[0]
            def_lo = def_old_str.split(',')[1]
            def_hi = ''.join(def_hi.split('.'))
            new = def_hi + '.' + def_lo
        return new
    else:
        def_hi = def_old_str.split('.')[0]
        def_lo = def_old_str.split('.')[1]
        def_hi = ''.join(def_hi.split(','))
        return def_hi + ',' + def_lo


def codify_int(p0, p1=2):
    def_ord = p1 - 1
    def_mag = 10 ** def_ord
    if p0 < def_mag:
        def_str = '0' * def_ord + str(p0)
    else:
        def_str = str(p0)
    return def_str

# main
# print(okinput())
# print(errorinput())
# print(title(p3=True))
# print(color.bckgreen(center('Wubba lubba dub dub!')))
# progressbarok()
# print(now())
# print(now())
# print(nowsep())