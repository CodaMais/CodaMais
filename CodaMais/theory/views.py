from django.shortcuts import render
from theory.models import Theory


def list_all_contents(request):
    content_list = Theory.objects.all().order_by('-id')
    return render(request,
                  'contents_page.html',
                  {'content_list': content_list})
