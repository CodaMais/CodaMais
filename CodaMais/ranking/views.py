# standard library
import logging

# Django.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Local Django
from user.models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@login_required
def show_ranking(request):
    data = {}
    logger.info("List users by score.")
    data['ranking'] = User.objects.filter().order_by('-score')
    return render(request, 'ranking.html', data)
