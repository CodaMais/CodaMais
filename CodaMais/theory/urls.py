from django.conf.urls import url, include

# Local Django
from .views import (
    list_all_theories,
    show_theory,
)

urlpatterns = (
    # Theory
    url(r'^redactor/', include('redactor.urls')),
    url(r'^theories/$', list_all_theories, name='theories'),
    url(r'^theory/(?P<id>\d+)/(?P<title>[\w|\W]+)/$', show_theory,
        name='show_theory'),
)
