from django.db import models
from main.models.expansion_set import ExpansionSet


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
    ]

    rarities = [
        ('free', 'Free'),
        ('common', 'Common'),
        ('rare', 'Rare'),
        ('epic', 'Epic'),
        ('legendary', 'Legendary'),
    ]

    card_types = [
        ('minion', 'Minion'),
        ('spell', 'Spell'),
        ('weapon', 'Weapon'),
        ('hero_card', 'Hero Card'),
    ]

    name = models.CharField(max_length=30, blank=False)
    card_type = models.CharField(max_length=9, blank=False, choices=card_types)
    hero_class = models.CharField(max_length=12, blank=True, choices=hero_classes)
    mana_cost = models.PositiveIntegerField(blank=False)
    rarity = models.CharField(max_length=9, blank=False, choices=rarities)
    image = models.ImageField(upload_to='card_images', blank=False)
    expansion_set = models.ForeignKey(ExpansionSet, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
