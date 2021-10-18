from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .constants import AGE_OF_MAJORITY, MAX_HUMAN_AGE
from .utils import get_age, get_todays_adult_dob

INVALID_FULL_NAME_ERROR = "Ensure you've entered your full name."
DOB_IN_FUTURE_ERROR = "Date of birth can't be in the future"
DOB_IN_DISTANT_PAST_ERROR = "Date of birth can't be in the distant past"
PERSON_DOES_NOT_EXIST_ERROR = "A person with username '%(username)s' does not exist"


def validate_full_name(value):
    if len(str(value).strip().split()) < 2:
        raise ValidationError(INVALID_FULL_NAME_ERROR)


def validate_date_of_birth(dob):
    age = get_age(dob=dob)
    if age < 0:
        raise ValidationError(DOB_IN_FUTURE_ERROR)

    if age > MAX_HUMAN_AGE:
        raise ValidationError(DOB_IN_DISTANT_PAST_ERROR)


def validate_adult(dob):
    if get_age(dob=dob) < AGE_OF_MAJORITY:
        raise ValidationError(f"Date of birth must be before {get_todays_adult_dob()}")


def validate_child(dob):
    if get_age(dob=dob) >= AGE_OF_MAJORITY:
        raise ValidationError(f"Date of birth must be after {get_todays_adult_dob()}")


def validate_person_username(username):
    try:
        from .models import Person

        Person.objects.get(username=username)
    except ObjectDoesNotExist:
        raise ValidationError(PERSON_DOES_NOT_EXIST_ERROR % dict(username=username))
