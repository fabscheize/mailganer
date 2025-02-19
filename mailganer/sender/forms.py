#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django import forms
from sender import models
from tinymce.widgets import TinyMCE

# class NewsletterForm(forms.Form):
#     subject = forms.CharField(max_length=255)
#     message = forms.CharField(widget=forms.Textarea)


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

        exclude = ('created_at',)
        labels = {
            'subject': 'Тема письма',
            'message': 'Сообщение',
        }
        help_texts = {
            'subject': 'Обязательное поле',
            'message': 'Обязательное поле',
        }
        widgets = {
            'message': forms.Textarea(
            # 'message': TinyMCE(
                {
                    'rows': 5,
                    'aria-describedby': 'id_textHelp',
                },
            ),
        }
        error_messages = {
            'subject': {
                'required': 'Пожалуйста, заполните тему письма',
            },
            'message': {
                'required': 'Пожалуйста, заполните Ваше сообщение',
            },
        }
