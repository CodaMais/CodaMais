from django.shortcuts import render
from .forms import UserRegisterForm
from .models import User


def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        username = form.cleaned_data.get('username')
        first_name = form.cleaned_data.get('first_name')
        User.objects.create_user(email=email, password=password,
                                 username=username, first_name=first_name)

    else:
        pass

    return render(request, "register_form.html", {"form": form})
