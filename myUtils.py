import time


def secToTime(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))
