import datetime


def week_days():
    now = datetime.datetime.now()
    now_day_1 = now - datetime.timedelta(days=now.weekday() + 14)
    dates = {}

    for n_week in range(3):
        dates[n_week] = [(now_day_1 + datetime.timedelta(days=d+n_week*7)).strftime("%Y-%m-%d") for d in range(7)]

    return dates