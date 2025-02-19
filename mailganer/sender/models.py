from __future__ import unicode_literals

from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(
        unique=True,
        )
    first_name = models.CharField(
        max_length=100,
        )
    last_name = models.CharField(
        max_length=100,
        )
    birthday = models.DateField()

    def __str__(self):
        return self.email
