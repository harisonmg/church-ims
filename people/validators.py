from django.core.exceptions import ValidationError

INVALID_FULL_NAME_ERROR = "Ensure you've entered your full name."


def validate_full_name(value):
    if len(str(value).strip().split()) < 2:
        raise ValidationError(INVALID_FULL_NAME_ERROR)
