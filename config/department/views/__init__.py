from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages
from department.decorators import security_decorator


@login_required(login_url='login')
@security_decorator
def base(request: WSGIRequest):
    return render(request, 'department/base.html')







def login_view(request: WSGIRequest):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request=request, user=user)
                return redirect('base')
            else:
                messages.error(request, "Login yoki parol xato", extra_tags="danger")
        else:
            messages.error(request, "Formani to'ldirishda xatolik yuz berdi", extra_tags='danger')

    return render(request, 'department/login.html', {

    })










