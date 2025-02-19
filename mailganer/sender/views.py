from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from sender.forms import NewsletterForm
from sender.models import Subscriber

def send_newsletter(request):
    template = 'sender/form.html'

    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            subscribers = Subscriber.objects.all()

            # for subscriber in subscribers:
            send_mail(
                subject,
                message,
                'from@example.com',
                [subscriber.email for subscriber in subscribers],
            )

            return JsonResponse({'status': 'success', 'message': 'The newsletter has been sent!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Form error!'})
    return render(request, template)
