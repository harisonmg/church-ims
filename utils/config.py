import re


def list_of_tuples(string):
    names = [s.strip("'") for s in re.findall(r"'\w+'", string)]
    emails = re.findall(r"\w+@\w+.\w+", string)
    return list(zip(names, emails))
