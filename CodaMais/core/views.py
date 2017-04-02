from django.shortcuts import render
from .forms import UserRegisterForm


def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
    else:
        pass

    return render(request, "register_form.html", {"form": form})
