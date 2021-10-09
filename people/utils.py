from datetime import date


def get_age(dob):
    today = date.today()
    age = today.year - dob.year
    age -= (today.month, today.day) < (dob.month, dob.day)
    return age
