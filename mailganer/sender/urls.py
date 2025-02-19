from django.conf.urls import url

from sender import views

app_name = 'sender'

urlpatterns = [
    url('', views.send_newsletter, name='send_newsletter'),
]
