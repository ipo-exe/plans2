# color functions


def bckgreen(p0='text'):
    color = '\033[1;30;42m' + p0 + '\033[m'
    return color


def bldgreen(p0='text'):
    color = '\033[1;32m' + p0 + '\033[m'
    return color


def bldblue(p0='text'):
    color = '\033[1;34m' + p0 + '\033[m'
    return color


def bldcyan(p0='text'):
    color = '\033[1;36m' + p0 + '\033[m'
    return color


def bldwhite(p0='text'):
    color = '\033[1m' + p0 + '\033[m'
    return color


def bckred(p0='text'):
    color = '\033[1;30;41m' + p0 + '\033[m'
    return color


def bckorage(p0='text'):
    color = '\033[1;30;43m' + p0 + '\033[m'
    return color


# print(bldwhite())
