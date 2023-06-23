import datetime
import math

def get_time_str():
    return datetime.datetime.now().strftime("%H:%M:%S:%f")


def angle_bound(angle):
    if angle > 180:
        return angle_bound(angle - 360)
    elif angle < -180:
        return angle_bound(angle + 360)
    else:
        return angle


