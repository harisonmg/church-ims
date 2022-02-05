from datetime import date, timedelta
from math import ceil

from django.core.exceptions import ObjectDoesNotExist

from thefuzz import fuzz

from . import constants

NEGATIVE_AGE_ERROR = "Age can't be negative!"
MAX_HUMAN_AGE_EXCEEDED_ERROR = f"Age shouldn't exceed {constants.MAX_HUMAN_AGE}!"

# age categories
CHILD = (0, constants.TEENAGE[0] - 1)
TEENAGER = constants.TEENAGE
YOUNG_ADULT = constants.YOUNG_ADULTHOOD
ADULT = (constants.YOUNG_ADULTHOOD[1] + 1, constants.MIDDLE_AGE[0] - 1)
MIDDLE_AGED = constants.MIDDLE_AGE
SENIOR_CITIZEN = (constants.AGE_OF_SENIORITY + 1, constants.MAX_HUMAN_AGE)


def get_age(dob):
    today = date.today()
    age = today.year - dob.year
    age -= (today.month, today.day) < (dob.month, dob.day)
    return age


def get_todays_adult_dob():
    days_lived = ceil(365.25 * constants.AGE_OF_MAJORITY)
    dob = date.today() - timedelta(days=days_lived)
    return dob


def get_age_category(age):
    if age < CHILD[0]:
        raise ValueError(NEGATIVE_AGE_ERROR)
    if age > SENIOR_CITIZEN[1]:
        raise ValueError(MAX_HUMAN_AGE_EXCEEDED_ERROR)

    age_category = None

    if age < TEENAGER[0]:
        age_category = "child"

    elif age < YOUNG_ADULT[0]:
        age_category = "teenager"

    elif age < ADULT[0]:
        age_category = "young adult"

    elif age < MIDDLE_AGED[0]:
        age_category = "adult"

    elif age < SENIOR_CITIZEN[0]:
        age_category = "middle-aged"

    elif age <= SENIOR_CITIZEN[1]:
        age_category = "senior citizen"

    return age_category


def get_personal_details(user):
    from .models import Person

    try:
        return Person.objects.get(user=user)
    except ObjectDoesNotExist:
        return None


def is_duplicate_person(person):
    from .models import Person

    queryset = Person.objects.filter(created_by=person.created_by)
    full_names = list(map(lambda p: p.full_name, queryset))
    for name in full_names:
        ratio = fuzz.token_set_ratio(person.full_name, name)
        if ratio == 100:
            return True
    return False


def is_duplicate_interpersonal_relationship(relationship):
    from .models import InterpersonalRelationship

    queryset = InterpersonalRelationship.objects.filter(person=relationship.person)
    queryset = queryset.filter(relative=relationship.relative)
    return queryset.count() > 0
