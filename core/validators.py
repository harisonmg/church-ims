from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .constants import AGE_OF_MAJORITY, MAX_HUMAN_LIFESPAN
from .utils import get_age


def validate_date_of_birth(value):
    """Raise a validation error if date of birth is in the future
    or is greater than the maximum human lifespan
    """
    age = get_age(value)
    if age < 0:
        raise ValidationError(_("Date of birth can't be in the future"))
    elif age > MAX_HUMAN_LIFESPAN:
        raise ValidationError(_("Age can't be greater than the maximum human lifespan"))


def validate_adult(value):
    """Raise a validation error if the current age is less than the
    age of majority
    """
    age = get_age(value)
    if age < AGE_OF_MAJORITY:
        raise ValidationError(_("Must be an adult"))


def validate_child(value):
    """Raise a validation error if the current age is greater
    than or equal to the age of majority
    """
    age = get_age(value)
    if age >= AGE_OF_MAJORITY:
        raise ValidationError(_("Must be a child"))
