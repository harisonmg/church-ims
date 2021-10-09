from people.models import Person


def search_people(search_term):
    username_matches = Person.objects.filter(username__icontains=search_term)
    full_name_matches = Person.objects.filter(full_name__icontains=search_term)
    return username_matches | full_name_matches
