#RGB
#################################################################
def rgb(text, R, G, B):
    if R > 255 or R < 0 or G > 255 or G < 0 or B > 255 or B < 0:
        raise ValueError(f'''
        Invalid RGB value at string: {italic(text)}
        RGB values should range from 0 to 255!
        ''')
    else:
        return f'\033[38;2;{R};{G};{B}m' + text + '\033[0m'
def rgbBgr(text, R, G, B):
    if R > 255 or R < 0 or G > 255 or G < 0 or B > 255 or B < 0:
        raise ValueError(f'''
        Invalid RGB value at string: {italic(text)}
        RGB values should range from 0 to 255!
        ''')
    else:
        return f'\033[48;2;{R};{G};{B}m' + text + '\033[0m'


#FORMATS
#################################################################
def bold(text):
    return '\033[1m' + text + '\033[0m'
def faint(text):
    return '\033[2m' + text + '\033[0m'
def italic(text):
    return '\033[3m' + text + '\033[0m'
def underline(text):
    return '\033[4m' + text + '\033[0m'
def slowblink(text):
    return '\033[5m' + text + '\033[0m'
def rapidblink(text):
    return '\033[6m' + text + '\033[0m'
def inverse(text):
    return '\033[7m' + text + '\033[0m'
def conceal(text):
    return '\033[8m' + text + '\033[0m'
def striketrough(text):
    return '\033[9m' + text + '\033[0m'
def doubleunderline(text):
    return '\033[21m' + text + '\033[0m'
def overline(text):
    return '\033[53m' + text + '\033[0m'


#COLOURS
#################################################################
def black(text):
    return '\033[30m' + text + '\033[0m'
def red(text):
    return '\033[31m' + text + '\033[0m'
def green(text):
    return '\033[32m' + text + '\033[0m'
def yellow(text):
    return '\033[33m' + text + '\033[0m'
def blue(text):
    return '\033[34m' + text + '\033[0m'
def purple(text):
    return '\033[35m' + text + '\033[0m'
def cyan(text):
    return '\033[36m' + text + '\033[0m'
def white(text):
    return '\033[37m' + text + '\033[0m'
def blackBgr(text):
    return '\033[40m' + text + '\033[0m'
def redBgr(text):
    return '\033[41m' + text + '\033[0m'
def greenBgr(text):
    return '\033[42m' + text + '\033[0m'
def yellowBgr(text):
    return '\033[43m' + text + '\033[0m'
def blueBgr(text):
    return '\033[44m' + text + '\033[0m'
def purpleBgr(text):
    return '\033[45m' + text + '\033[0m'
def cyanBgr(text):
    return '\033[46m' + text + '\033[0m'
def whiteBgr(text):
    return '\033[47m' + text + '\033[0m'
def brightblack(text):
    return '\033[90m' + text + '\033[0m'
def brightred(text):
    return '\033[91m' + text + '\033[0m'
def brightgreen(text):
    return '\033[92m' + text + '\033[0m'
def brightyellow(text):
    return '\033[93m' + text + '\033[0m'
def brightblue(text):
    return '\033[94m' + text + '\033[0m'
def brightpurple(text):
    return '\033[95m' + text + '\033[0m'
def brightcyan(text):
    return '\033[96m' + text + '\033[0m'
def brightwhite(text):
    return '\033[97m' + text + '\033[0m'
def brightblackBgr(text):
    return '\033[100m' + text + '\033[0m'
def brightredBgr(text):
    return '\033[101m' + text + '\033[0m'
def brightgreenBgr(text):
    return '\033[102m' + text + '\033[0m'
def brightyellowBgr(text):
    return '\033[103m' + text + '\033[0m'
def brightblueBgr(text):
    return '\033[104m' + text + '\033[0m'
def brightpurpleBgr(text):
    return '\033[105m' + text + '\033[0m'
def brightcyanBgr(text):
    return '\033[106m' + text + '\033[0m'
def brightwhiteBgr(text):
    return '\033[107m' + text + '\033[0m'
