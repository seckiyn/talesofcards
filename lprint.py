from colorama import init, Fore, Style


def red(string):
    return Fore.RED + str(string) + Style.RESET_ALL
def yellow(string):
    return Fore.YELLOW + str(string) + Style.RESET_ALL
def blue(string):
    return Fore.BLUE + str(string)+ Style.RESET_ALL

# colorama
init()

DEBUG = True
def print_debug(*args, level=1, **kwargs):
    #TODO: add levels of debug
    if DEBUG:
        print(Fore.YELLOW+"[DEBUG]"+Style.RESET_ALL, *args, **kwargs)

def print_error(*args, **kwargs):
    print(red("[ERROR]"), *args, **kwargs)
