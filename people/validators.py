from django.core.exceptions import ValidationError

from .constants import MAX_HUMAN_AGE
from .utils import get_age

INVALID_FULL_NAME_ERROR = "Ensure you've entered your full name."
DOB_IN_FUTURE_ERROR = "Date of birth can't be in the future"
DOB_IN_DISTANT_PAST_ERROR = "Date of birth can't be in the distant past"


def validate_full_name(value):
    if len(str(value).strip().split()) < 2:
        raise ValidationError(INVALID_FULL_NAME_ERROR)


def validate_date_of_birth(dob):
    age = get_age(dob=dob)
    if age < 0:
        raise ValidationError(DOB_IN_FUTURE_ERROR)

    if age > MAX_HUMAN_AGE:
        raise ValidationError(DOB_IN_DISTANT_PAST_ERROR)
