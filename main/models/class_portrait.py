from django.db import models


class ClassPortrait(models.Model):
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
        ('warrior', 'Warrior')
    ]

    name = models.CharField(max_length=20, blank=False)
    image = models.ImageField(upload_to='class_portrait_images', blank=False)
    hero_class = models.CharField(max_length=12, blank=True, choices=hero_classes)

    def __str__(self):
        return self.name
