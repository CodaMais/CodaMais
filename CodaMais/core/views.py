from django.shortcuts import render
from .forms import UserRegisterForm


def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
    else:
        pass

    return render(request, "register_form.html", {"form": form})
