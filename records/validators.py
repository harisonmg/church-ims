from . import constants

INVALID_HUMAN_BODY_TEMP_ERROR = "Invalid human body temperature!"


def human_body_temperature_validator(value):
    if value > constants.MAX_HUMAN_BODY_TEMP:
        raise ValueError(INVALID_HUMAN_BODY_TEMP_ERROR)

    if value < constants.MIN_HUMAN_BODY_TEMP:
        raise ValueError(INVALID_HUMAN_BODY_TEMP_ERROR)
    return None
