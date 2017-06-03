from django.shortcuts import render
from django.shortcuts import redirect


def home(request):
    if request.user.is_authenticated():
        return redirect('/dashboard/dashboard')
    else:
        # Nothing to do
        pass

    return render(request, 'index.html')


def about(request):

    return render(request, 'about.html')
