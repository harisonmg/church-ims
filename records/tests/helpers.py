from records.models import TemperatureRecord


def search_temperature_records(search_term):
    username_matches = TemperatureRecord.objects.filter(
        person__username__icontains=search_term
    )
    full_name_matches = TemperatureRecord.objects.filter(
        person__full_name__icontains=search_term
    )
    return username_matches | full_name_matches
