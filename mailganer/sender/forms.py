# -*- coding: utf-8 -*-

from django import forms
from sender import models
from tinymce.widgets import TinyMCE


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
            if field.errors:
                field.field.widget.attrs['class'] += ' is-invalid'

    class Meta:
        abstract = True


class NewsletterForm(BaseModelForm):

    class Meta:
        model = models.Newsletter

        exclude = (
            'created_at',
            'reached_subs',
            'read_subs',
        )
        labels = {
            'subject': 'Тема письма',
            'message': 'Сообщение',
        }
        help_texts = {
            'message': 'Для персонализации сообщения выберете переменную нажав на значок тега в панели инструментов',
        }
        widgets = {'message': TinyMCE()}
        error_messages = {
            'subject': {
                'required': 'Пожалуйста, заполните тему письма',
            },
            'message': {
                'required': 'Пожалуйста, заполните Ваше сообщение',
            },
        }
