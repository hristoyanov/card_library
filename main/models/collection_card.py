from django.contrib.auth.models import User
from django.db import models
from main.models.card import Card


class CollectionCard(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    copies = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.card.name
