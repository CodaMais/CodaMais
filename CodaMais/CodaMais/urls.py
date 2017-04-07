"""CodaMais URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from exercise.views import *
from django.views.static import serve
from django.conf.urls import include


urlpatterns = [
    url(r'^exercise/(?P<id>\d+)/$', show_exercise, name='show_exercise'),
    url(r'^exercise/$', list_exercises_not_deprecated, name='list_exercises_not_deprecated'),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^admin/', admin.site.urls),
]

# When using the Django's dev server, static files are served by default but
# not media files, so you here we're force the server to consider them
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
]
