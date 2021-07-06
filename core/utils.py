from datetime import date


def get_age(value):
    today = date.today()
    age = today.year - value.year
    age -= (today.month, today.day) < (value.month, value.day)
    return age
