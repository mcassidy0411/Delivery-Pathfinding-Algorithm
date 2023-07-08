# Michael Cassidy, 009986687

import datetime


def parse_time_string(time):
    try:
        hours, minutes = time.split(":")
        return datetime.datetime.now().replace(hour=int(hours), minute=int(minutes), second=0, microsecond=0)
    except AttributeError:
        return None
