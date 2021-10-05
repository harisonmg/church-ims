def format_people_details(people):
    search_results = {}
    for i, person in enumerate(people):
        search_results[str(i + 1)] = [person.username, person.full_name, "add temp"]
    return search_results


def find_people_by_name(people, name):
    search_results = []
    for person in people:
        if name.lower() in person.full_name.lower():
            search_results.append(person)
    return format_people_details(search_results)
