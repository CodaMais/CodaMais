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
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

# Local Django
from user import views

urlpatterns = i18n_patterns(
    url(r'^admin/', admin.site.urls),
    # TODO(João) Change this url to landpage, and delete this url
    url(r'^register/', views.register_view, name='register_view'),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm,
        name='confirm_account'),
    # TODO(João) Change this url to landpage, and delete this url
    url(r'^login/', views.login_view, name='login_view'),
)
