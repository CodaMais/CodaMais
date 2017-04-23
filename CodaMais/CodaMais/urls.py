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


# Django
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.static import serve
from django.conf.urls import include
from django.contrib.auth.decorators import login_required


# Local Django
from user import views
from exercise.views import show_exercise
from exercise.views import list_exercises_not_deprecated
from landing.views import home
from dashboard.views import dashboard

urlpatterns = i18n_patterns(
    url(r'^$', home, name="landing_home"),
    url(r'^admin/', admin.site.urls),
    # TODO(João) Change this url to landpage, and delete this url
    url(r'^register/', views.register_view, name='register_view'),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm,
        name='confirm_account'),
    url(r'^dashboard/', login_required(dashboard), name='dashboard'),
    # Recover password.
    url(r'^recoverpassword/', views.recover_password, name='recover_password'),
    url(r'^recover/(?P<activation_key>\w+)/', views.recover_password_confirm,
        name='recover_password_confirm'),
    # TODO(João) Change this url to landpage, and delete this url
    url(r'^login/', views.login_view, name='login_view'),
    url(r'^logout/', views.logout_view, name='logout_view'),
    # Exercise.
    url(r'^exercise/(?P<id>\d+)/$', show_exercise, name='show_exercise'),
    url(r'^exercise/$', list_exercises_not_deprecated,
        name='list_exercises_not_deprecated'),
    url(r'^redactor/', include('redactor.urls')),
)

# When using the Django's dev server, static files are served by default but
# not media files, so you here we're force the server to consider them
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
        ]
