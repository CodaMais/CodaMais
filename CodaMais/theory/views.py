from django.shortcuts import render
from theory.models import Theory


def list_all_theories(request):
    theory_list = Theory.objects.all().order_by('-id')
    return render(request,
                  'theories_page.html',
                  {'theory_list': theory_list})


def show_theory(request, id, title):
    theory = Theory.objects.get(id=id)
    return render(request, 'theory_details.html', {'theory': theory})
