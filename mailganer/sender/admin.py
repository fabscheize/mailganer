from django.contrib import admin

from sender import models


@admin.register(models.Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'first_name',
        'last_name',
        'birthday',
    )


@admin.register(models.Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'created_at',
    )
    readonly_fields = (
        'created_at',
        'subject',
        'message',
        'reached_subs',
        'read_subs',
    )
