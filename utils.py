import datetime

def get_time_str():
    return datetime.datetime.now().strftime("%H:%M:%S:%f")