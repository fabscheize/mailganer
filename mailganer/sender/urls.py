from django.conf.urls import url

from sender import views

app_name = 'sender'

urlpatterns = [
    url('', views.NewsletterView.as_view(), name='newsletter'),
]
