from django.conf.urls import url

from sender import views

app_name = 'sender'

urlpatterns = [
    url(r'^newsletter/track$', views.NewsletterTrackView.as_view(), name='read'),
    url(r'^newsletter/(?P<newsletter_id>[0-9]+)/$', views.NewsletterDetailView.as_view(), name='newsletter'),
    url(r'^$', views.MainView.as_view(), name='main'),
]
