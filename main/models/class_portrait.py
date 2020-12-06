from django.db import models


class ClassPortrait(models.Model):
    name = models.CharField(max_length=20, blank=False)
    image = models.ImageField(upload_to='class_portrait_images', blank=False)

    def __str__(self):
        return self.name
