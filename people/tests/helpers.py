from people.models import InterpersonalRelationship, Person


def search_people(search_term):
    username_matches = Person.objects.filter(username__icontains=search_term)
    full_name_matches = Person.objects.filter(full_name__icontains=search_term)
    return username_matches | full_name_matches


def search_interpersonal_relationships(search_term):
    person_matches = InterpersonalRelationship.objects.filter(
        person__username__icontains=search_term
    )
    relative_matches = InterpersonalRelationship.objects.filter(
        relative__username__icontains=search_term
    )
    return person_matches | relative_matches
