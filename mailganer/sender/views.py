from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from sender.forms import NewsletterForm
from sender.models import Subscriber, Newsletter
import django.views.generic
import django.db
import django.shortcuts
from django.core.urlresolvers import reverse

class NewsletterView(
    django.views.generic.base.TemplateResponseMixin,
    django.views.generic.View,
):
    template_name = 'sender/newsletter.html'

    def get(self, request, *args, **kwargs):
        all_newsletters = Newsletter.objects.order_by('-created_at')
        form = NewsletterForm()
        return self.render_to_response(
            {"newsletters": all_newsletters, "form": form}
        )

    def post(self, request, *args, **kwargs):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            with django.db.transaction.atomic():
                new_letter = form.save(commit=False)
                new_letter.save()

            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            subscribers = Subscriber.objects.all()
            print(new_letter.subject, new_letter.message)
            print(subject, message)
            print(subscribers)
            # for subscriber in subscribers:
            send_mail(
                new_letter.subject,
                new_letter.message,
                'from@example.com',
                [subscriber.email for subscriber in subscribers],
            )

            return django.shortcuts.redirect(
                reverse("sender:newsletter"),
            )

        all_newsletters = Newsletter.objects.order_by('-created_at')
        return self.render_to_response(
            {"newsletters": all_newsletters, "form": form}
        )
