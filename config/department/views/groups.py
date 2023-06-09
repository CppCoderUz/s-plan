from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required
from department.decorators import not_source_URL, security_decorator
from department.forms import SmallGroupFullForm, SmallGroupForm
from curriculum.models import Direction, SmallGroup






@login_required(login_url='login')
@security_decorator
def groups_all(request: WSGIRequest):
    search = request.GET.get('search', None)
    language = request.GET.get('language', None)
    study_form = request.GET.get('form', None) 
    year = request.GET.get('year', None)

    data = SmallGroup.objects.all().order_by('-pk')
    if search:
        data = data.filter(direction__name__contains=search)
    if language:
        data = data.filter(direction__language=language)
    if study_form:
        data = data.filter(direction__study_form=study_form)
    if year:
        data = data.filter(direction__year=year)

    return render(request, 'department/groups/all.html', {
        'data': data,
    })



@login_required(login_url='login')
@security_decorator
def detail_group(request: WSGIRequest, pk):
    object = get_object_or_404(SmallGroup, pk=pk)

    form = SmallGroupForm(instance=object)
    return render(request, 'department/groups/detail.html', {
        'object': object,
        'form': form,
    })



@security_decorator
@not_source_URL
def delete_group(request: WSGIRequest, pk):
    object = get_object_or_404(SmallGroup, pk=pk)
    object.delete()
    return redirect('d_groups_all')


@security_decorator
@not_source_URL
def change_group(request: WSGIRequest, pk):
    object = get_object_or_404(SmallGroup, pk=pk)
    form = SmallGroupForm(instance=object, data=request.POST)
    if form.is_valid:
        form.save()
    return redirect('d_detail_group', pk=pk)
    
    