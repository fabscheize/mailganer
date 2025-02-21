from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.template import Template, Context
from sender.forms import NewsletterForm
from sender.models import Subscriber, Newsletter
import django.views.generic
import django.db
import django.shortcuts
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from io import BytesIO
from PIL import Image

TEMPLATE_HEAD = '<html><body>'
TEMPLATE_TAIL = '<img src="http://localhost:8000/newsletter/track?newsletter_id={{newsletter_id}}&subscriber_id={{subscriber_id}}" width="1" height="1" /></body></html>'


class MainView(
    django.views.generic.base.TemplateResponseMixin,
    django.views.generic.View,
):
    template_name = 'sender/main.html'

    def get(self, request, *args, **kwargs):
        all_newsletters = Newsletter.objects.order_by('-created_at')
        form = NewsletterForm()
        return self.render_to_response(
            {"newsletters": all_newsletters, "form": form}
        )

    def post(self, request, *args, **kwargs):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subscribers = Subscriber.objects.all()

            with django.db.transaction.atomic():
                new_letter = form.save(commit=False)
                new_letter.reached_subs = subscribers.count()
                new_letter.save()

            message = TEMPLATE_HEAD + new_letter.message + TEMPLATE_TAIL
            print(message)
            template = Template(message)

            for subscriber in subscribers:
                html_message = template.render(
                    Context(
                        {
                            'first_name': subscriber.first_name,
                            'last_name': subscriber.last_name,
                            'birthday': subscriber.birthday,
                            'email': subscriber.email,
                            'newsletter_id': new_letter.id,
                            'subscriber_id': subscriber.id,
                        }
                    )
                )
                print(new_letter.id)
                print(subscriber.id)
                send_mail(
                    new_letter.subject,
                    html_message,
                    'from@example.com',
                    [subscriber.email],
                    html_message=html_message,
                )

            return django.shortcuts.redirect(
                reverse("sender:main"),
            )

        all_newsletters = Newsletter.objects.order_by('-created_at')
        return self.render_to_response(
            {"newsletters": all_newsletters, "form": form}
        )


class NewsletterDetailView(django.views.generic.detail.DetailView):
    model = Newsletter
    template_name = "sender/detail.html"
    pk_url_kwarg = 'newsletter_id'

    def get_object(self, queryset=None):
        return super(NewsletterDetailView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(NewsletterDetailView, self).get_context_data(**kwargs)
        newsletter = self.object

        viewed_subscribers = newsletter.read_subs.all()

        context['viewed_subscribers'] = viewed_subscribers
        context['viewed_subscribers_count'] = viewed_subscribers.count()
        context['reached_subs_count'] = newsletter.reached_subs

        return context


class NewsletterTrackView(
    django.views.generic.View,
):
    def get(self, request, *args, **kwargs):
        newsletter_id = request.GET.get('newsletter_id')
        subscriber_id = request.GET.get('subscriber_id')

        current_newsletter = get_object_or_404(Newsletter, id=newsletter_id)
        current_subscriber = get_object_or_404(Subscriber, id=subscriber_id)

        with django.db.transaction.atomic():
            if current_subscriber not in current_newsletter.read_subs.all():
                current_newsletter.read_subs.add(current_subscriber)
                current_newsletter.save()

        image = Image.new("RGB", (1, 1), color=(255, 255, 255))
        response = HttpResponse(content_type="image/png")
        image.save(response, format="PNG")

        response["Cache-Control"] = "no-cache"
        response["Content-Disposition"] = "inline; filename=tracking_pixel.png"
        return response
