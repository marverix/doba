import math
import time


def time_str() -> str:
    """
    Create a time string in format YYYYMMDD-HHMMSSsssTTTT
    :return:
    """
    time_s = time.strftime("%Y%m%d-%H%M%S{}%z")
    ms = math.floor(math.modf(time.time())[0]*1000)
    return time_s.format(ms)
