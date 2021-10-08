INVALID_FULL_NAME_ERROR = "Ensure you've entered your full name."


def full_name_validator(value):
    if len(str(value).strip().split()) < 2:
        raise ValueError(INVALID_FULL_NAME_ERROR)
    return None
