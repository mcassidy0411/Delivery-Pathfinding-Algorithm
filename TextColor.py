class TextColor:
    text_color_dict = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        'reset': '\033[0m'
    }

    def blue(self):
        return self.text_color_dict['blue']

    def black(self):
        return self.text_color_dict['black']

    def red(self):
        return self.text_color_dict['red']

    def green(self):
        return self.text_color_dict['green']

    def yellow(self):
        return self.text_color_dict['yellow']

    def magenta(self):
        return self.text_color_dict['magenta']

    def cyan(self):
        return self.text_color_dict['cyan']

    def white(self):
        return self.text_color_dict['white']

    def bright_black(self):
        return self.text_color_dict['bright_black']

    def bright_red(self):
        return self.text_color_dict['bright_red']

    def bright_green(self):
        return self.text_color_dict['bright_green']

    def bright_yellow(self):
        return self.text_color_dict['bright_yellow']

    def bright_blue(self):
        return self.text_color_dict['bright_blue']

    def bright_magenta(self):
        return self.text_color_dict['bright_magenta']

    def bright_cyan(self):
        return self.text_color_dict['bright_cyan']

    def bright_white(self):
        return self.text_color_dict['bright_white']

    def reset(self):
        return self.text_color_dict['reset']