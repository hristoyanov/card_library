from django.db import models
from main.models.card import Card
from main.models.custom_user import CustomUser


class CollectionCard(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    copies = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.card.name
