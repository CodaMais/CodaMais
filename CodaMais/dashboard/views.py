from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


@login_required()
def dashboard(request):

    return render(request, 'dashboard.html')


# This method is called when the aplication raises a 404 error and replace the debug
# 404 error default page for a customized one (404.html).
def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response
