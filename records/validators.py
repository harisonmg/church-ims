from django.core.exceptions import ValidationError

from . import constants

INVALID_HUMAN_BODY_TEMP_ERROR = "Invalid human body temperature!"


def validate_human_body_temperature(value):
    if value > constants.MAX_HUMAN_BODY_TEMP:
        raise ValidationError(INVALID_HUMAN_BODY_TEMP_ERROR)

    if value < constants.MIN_HUMAN_BODY_TEMP:
        raise ValidationError(INVALID_HUMAN_BODY_TEMP_ERROR)
