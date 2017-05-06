# Django.
from django.conf.urls import url

# Local Django
from .views import (
    show_ranking,
)

urlpatterns = (
    # Ranking
    url(r'^ranking/$', show_ranking, name='show_ranking'),
)
