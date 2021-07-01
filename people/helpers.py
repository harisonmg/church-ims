from django.contrib.auth import get_user_model


# TODO: check if request.user can be used in get
def get_user_profile(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    return user.person
