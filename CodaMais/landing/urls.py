# Django.
from django.conf.urls import url

# Local Django.
from .views import about

urlpatterns = (
    # Forum
    url(r'^$', about, name='about'),
)
