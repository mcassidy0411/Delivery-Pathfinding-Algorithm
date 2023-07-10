# Michael Cassidy, 009986687

import datetime


# Helper function takes a string as input and attempts to convert it to a datetime object.  If unable, returns None.
# O(1)
def parse_time_string(time):
    try:
        hours, minutes = time.split(":")
        return datetime.datetime.now().replace(hour=int(hours), minute=int(minutes), second=0, microsecond=0)
    except AttributeError:
        return None
