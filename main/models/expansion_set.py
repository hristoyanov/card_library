from django.db import models


class ExpansionSet(models.Model):
    name = models.CharField(max_length=50, blank=False)
    card_count = models.PositiveIntegerField(blank=False)
    image = models.ImageField(upload_to='card_set_images', blank=False)
    release_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
