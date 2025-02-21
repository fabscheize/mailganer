#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.db import models

from tinymce import models as tinymce_models


class Subscriber(models.Model):
    email = models.EmailField(
        'электронная почта',
        unique=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=100,
    )
    last_name = models.CharField(
        'фамилия',
        max_length=100,
    )
    birthday = models.DateField(
        'день рождения',
    )

    class Meta:
        verbose_name = 'подписчик'
        verbose_name_plural = 'подписчики'

    def __str__(self):
        return self.email if len(self.email) <= 21 else self.email[:18] + '...'



class Newsletter(models.Model):
    created_at = models.DateTimeField(
        'дата создания',
        auto_now_add=True,
        null=True,
    )
    subject = models.CharField(
        'тема',
        max_length=100,
    )
    message = tinymce_models.HTMLField(
        'сообщение',
    )
    reached_subs = models.IntegerField(
        verbose_name='количество получивших рассылку',
        default=0,
    )
    read_subs = models.ManyToManyField(
        Subscriber,
        verbose_name='прочитавшие подписчики',
    )

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

    def __str__(self):
        return self.subject if len(self.subject) <= 21 else self.subject[:18] + '...'
