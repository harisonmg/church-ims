import string

import decouple


def list_of_tuples(config_string):
    strip_chars = string.whitespace + "[]()"
    config = decouple.Csv(strip=strip_chars)(config_string)
    names = config[::2]
    emails = list(reversed(config[::-2]))
    return list(zip(names, emails))
