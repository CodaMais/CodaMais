# standard library
import logging

# third-party
import hashlib
import datetime
import random

# Django
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponse

# local Django
from .forms import UserRegisterForm
from .models import User
from .models import UserProfile
from . import constants

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register_view(request):
    form = UserRegisterForm(request.POST or None)
    logger.info("Rendering Register Page.")
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        username = form.cleaned_data.get('username')
        first_name = form.cleaned_data.get('first_name')
        User.objects.create_user(email=email, password=password,
                                 username=username, first_name=first_name)

        # Prepare the information needed to send the account verification
        # email.
        salt = hashlib.sha1(str(random.random()).
                            encode('utf-8')).hexdigest()[:5]
        activation_key = hashlib.sha1(str(salt+email).
                                      encode('utf‌​-8')).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)

        user = User.objects.get(username=username)

        new_profile = UserProfile(user=user, activation_key=activation_key,
                                  key_expires=key_expires)
        new_profile.save()

        # Send account confirmation email.
        email_subject = (constants.EMAIL_CONFIRMATION_SUBJECT)
        email_body = constants.EMAIL_CONFIRMATION_BODY % (username,
                                                          activation_key)

        send_mail(email_subject, email_body, constants.CODAMAIS_EMAIL, [email],
                  fail_silently=False)

        return render(request, "register_sucess.html")

    else:
        logger.info("Register form was invalid.")

    return render(request, "register_form.html", {"form": form})


def register_confirm(request, activation_key):
    # Verify if user is already logged.
    if request.user.is_authenticated():
        HttpResponse('Conta ja confirmada')
    else:
        # Nothing to do
        pass

    # Check if activation token is valid, if not valid return an 404 error.
    user_profile = get_object_or_404(UserProfile,
                                     activation_key=activation_key)

    # Verifies if the activation token has expired and if so renders the html
    # of expired registration.

    if user_profile.key_expires < timezone.now():
        return render_to_response('user_profile/confirm_expired.html')
    else:
        # Nothing to do.
        pass

    # If the token has not expired, the user is activated and the
    # confirmation html is displayed.

    user = user_profile.user
    user.is_active = True
    user.save()

    return render_to_response('confirmed_account.html')
