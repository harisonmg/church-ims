import re

from people.tests import helpers as people_helpers
from records.tests import helpers as records_helpers

from . import formatting


def find_url(text):
    return re.search(r"(?P<url>https?://[^\s]+)", text).group("url")


def search_people(search_term):
    search_results = people_helpers.search_people(search_term=search_term)
    return formatting.format_people_list(search_results)


def search_temperature_records(search_term):
    search_results = records_helpers.search_temperature_records(search_term=search_term)
    return formatting.format_temperature_records(search_results)
