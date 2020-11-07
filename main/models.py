from django.db import models


# Create your models here.
class ExpansionSet(models.Model):
    name = models.CharField(max_length=50, blank=False)
    card_count = models.PositiveIntegerField(blank=False)
    image_url = models.URLField(blank=False)


class Card(models.Model):
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
        ('neutral', 'Neutral'),
    ]

    rarities = [
        ('free', 'Free'),
        ('common', 'Common'),
        ('rare', 'Rare'),
        ('epic', 'Epic'),
        ('legendary', 'Legendary'),
    ]

    name = models.CharField(max_length=30, blank=False)
    hero_class = models.CharField(max_length=12, blank=False, choices=hero_classes)
    mana_cost = models.PositiveIntegerField(blank=False)
    rarity = models.CharField(max_length=9, blank=False, choices=rarities)
    image_url = models.URLField(blank=False)
    expansion_set = models.ForeignKey(ExpansionSet, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
