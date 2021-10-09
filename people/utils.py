from datetime import date

from . import constants

NEGATIVE_AGE_ERROR = "Age can't be negative!"
MAX_HUMAN_AGE_EXCEEDED_ERROR = f"Age shouldn't exceed {constants.MAX_HUMAN_AGE}!"


def get_age(dob):
    today = date.today()
    age = today.year - dob.year
    age -= (today.month, today.day) < (dob.month, dob.day)
    return age


def get_age_category(age):
    if age < 0:
        raise ValueError(NEGATIVE_AGE_ERROR)
    elif age < constants.TEENAGE[0] - 1:
        return "child"
    elif age < constants.YOUNG_ADULTHOOD[0]:
        return "teenager"
    elif age < constants.YOUNG_ADULTHOOD[1] + 1:
        return "young adult"
    elif age < constants.MIDDLE_AGE[0] - 1:
        return "adult"
    elif age < constants.AGE_OF_SENIORITY:
        return "middle-aged"
    elif age <= constants.MAX_HUMAN_AGE:
        return "senior citizen"
    else:
        raise ValueError(MAX_HUMAN_AGE_EXCEEDED_ERROR)
