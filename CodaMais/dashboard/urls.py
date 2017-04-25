# Django.
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

# Local Django.
from dashboard.views import dashboard

urlpatterns = (
    url(r'^dashboard/', login_required(dashboard), name='dashboard'),
)
