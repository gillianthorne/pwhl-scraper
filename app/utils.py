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
    return datetime.datetime.strptime(date_str, "%a, %b %d")