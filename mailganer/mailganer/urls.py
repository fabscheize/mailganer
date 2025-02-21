from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('sender.urls')),
    url('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        url(
            "__debug__/",
            include(debug_toolbar.urls),
        ),
    )
