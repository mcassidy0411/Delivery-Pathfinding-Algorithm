# Michael Cassidy, 009986687

# Reference to convert color escape sequences into more meaningful words.  Used to adjust the text color of data
# printed to the console O(1)
class TextColor:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    magenta = '\033[35m'
    cyan = '\033[36m'
    white = '\033[37m'
    bright_black = '\033[90m'
    bright_red = '\033[91m'
    bright_green = '\033[92m'
    bright_yellow = '\033[93m'
    bright_blue = '\033[94m'
    bright_magenta = '\033[95m'
    bright_cyan = '\033[96m'
    bright_white = '\033[97m'
    reset = '\033[0m'
