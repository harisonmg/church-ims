from django.db.models.signals import post_save
from django.dispatch import receiver

from people.models import Person

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_person(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)
