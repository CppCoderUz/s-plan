
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required
from department.decorators import not_source_URL, security_decorator

from accounts.models import User

def logout_view(request: WSGIRequest):
    logout(request)
    redirect('login')




@security_decorator
@not_source_URL
def check_username(request: WSGIRequest):
    q = request.POST.get('q', None)
    if not q:
        return HttpResponse('false')
    if len(q) < 5:
        return HttpResponse('false')
    try:
        User.objects.get(username=q)
        return HttpResponse('false')
    except:
        return HttpResponse('true')

