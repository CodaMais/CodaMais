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

# Django.
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf.urls.i18n import i18n_patterns
# from django.template.response import TemplateResponse


# Local Django
from landing.views import home

urlpatterns = i18n_patterns(
    url('^user/', include('user.urls')),
    url('^exercise/', include('exercise.urls')),
    url('^forum/', include('forum.urls')),
    url('^theory/', include('theory.urls')),
    url(r'^$', home, name="landing_home"),
    url(r'^admin/', admin.site.urls),
    url(r'^about/', include('landing.urls')),
    # When using the Django's dev server, static files are served by default but
    # not media files, so you here we're force the server to consider them.
    url('^dashboard/', include('dashboard.urls')),
    url('^ranking/', include('ranking.urls')),
)

# When using the Django's dev server, static files are served by default but
# not media files, so you here we're force the server to consider them
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
        # url(r'^', TemplateResponse, {'template': '404.html'}),
    ]
