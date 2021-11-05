from datetime import date


def format_temperature(temperature):
    return "{:.2f}\N{DEGREE SIGN}C".format(temperature)


def is_duplicate_temp_record(temp_record):
    from .models import TemperatureRecord

    creation_date = date.today()
    if temp_record.created_at is not None:
        creation_date = temp_record.created_at.date()

    queryset = TemperatureRecord.objects.filter(person=temp_record.person)
    queryset = queryset.filter(created_at__date=creation_date)
    return queryset.count() > 0
