from django.http import Http404
from django.core.handlers.wsgi import WSGIRequest
from accounts.models import DepartmentEmployee
from accounts.groups import DEPARTMENT




def security_decorator(func):
    def wrapper_func(request: WSGIRequest, *args, **kwargs):
        user = request.user
        if not request.user.is_authenticated:
            raise Http404
        try:
            employee = DepartmentEmployee.objects.get(user_id=request.user.pk)
            employee.user.groups.get(name=DEPARTMENT.name)
        except:
            raise Http404
        
        return func(request, *args, **kwargs)
    return wrapper_func



def not_source_URL(func):
    def wrapper_func(request: WSGIRequest, *args, **kwargs):
        if not (request.method == 'POST'):
            raise Http404
        if request.POST.get('csrfmiddlewaretoken', False) == False:
            raise Http404
        return func(request, *args, **kwargs)
    return wrapper_func




