from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models.class_portrait import ClassPortrait
from main_auth.models import UserProfile
from django.contrib.auth.models import Group


@receiver(post_save, sender=User)
def user_created(sender, instance, created, *args, **kwargs):
    if created:
        if not instance.is_superuser:
            profile = UserProfile(user=instance, profile_picture=ClassPortrait.objects.get(name='Default'))
            profile.save()
        else:
            profile = UserProfile(user=instance)
            profile.save()
