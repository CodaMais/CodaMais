from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse


@login_required()
def dashboard(request):

    return render(request, 'dashboard.html')


def user_exercise_chart(request):
    data = {
            'labels': ['20/JPN - 30/Jan', '20/Feb - 20/Feb', '20/Mar - 20/Mar', '20/Abr - 20/Abr', '20/Mai - 20/Mai'],
            'series': [
                [542, 443, 320, 600, 553],
                [412, 243, 280, 580, 453]
              ]
          }

    return JsonResponse(data)
