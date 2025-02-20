from __future__ import unicode_literals

from django.db import models

from tinymce import models as tinymce_models


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


class Newsletter(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    subject = models.CharField(
        max_length=100,
    )
    message = tinymce_models.HTMLField()
    # message = models.TextField()
