from django.db import models


class CustomUser(models.Model):
    username = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.username
