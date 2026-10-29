import datetime


def format_time(raw_time):
    return f"00:{raw_time}"

def parse_game_time(time_str, am_pm):
    if time_str[1] == ":":
        time_str = f"0{time_str}"

    time_datetime = datetime.datetime.strptime(time_str, "%I:%M")

    if am_pm == "pm":
        time_datetime += datetime.timedelta(hours = 12)

    time_str_proper = datetime.datetime.strftime(time_datetime, "%H:%M")

    return time_str_proper

def parse_date(date_str):
    return str(datetime.datetime.strptime(date_str, "%a, %b %d"))

def parse_duration(duration_str):
    hours_str, minutes_str = duration_str.split(":")
    hours = int(hours_str)
    minutes = int(minutes_str)

    # normalize in case minutes ever overflow 60 (e.g. summed durations)
    if minutes >= 60:
        hours += minutes // 60
        minutes = minutes % 60

    return f"{hours:02d}:{minutes:02d}:00"