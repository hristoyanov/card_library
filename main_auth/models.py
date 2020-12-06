from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from main.models.class_portrait import ClassPortrait


class UserProfile(models.Model):
    hero_classes = [
        ('demon_hunter', 'Demon Hunter'),
        ('druid', 'Druid'),
        ('hunter', 'Hunter'),
        ('mage', 'Mage'),
        ('paladin', 'Paladin'),
        ('priest', 'Priest'),
        ('rogue', 'Rogue'),
        ('shaman', 'Shaman'),
        ('warlock', 'Warlock'),
        ('warrior', 'Warrior'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ForeignKey(ClassPortrait, blank=True, on_delete=models.DO_NOTHING)
    favourite_class = models.CharField(max_length=12, choices=hero_classes, blank=True)

    def __str__(self):
        return self.user.username
