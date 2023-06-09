from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from curriculum.models import Direction, SmallGroup

from department.decorators import not_source_URL, security_decorator
from department.forms import DirectionForm, SmallGroupForm


@login_required(login_url='login')
@security_decorator
def all_direction(request: WSGIRequest):
    search = request.GET.get('search', None)
    language = request.GET.get('language', None)
    study_form = request.GET.get('form', None)
    year = request.GET.get('year', None)

    data = Direction.objects.all()
    if search:
        data = data.filter(name__contains=search)
    if language:
        data = data.filter(language=language)
    if study_form:
        data = data.filter(study_form=study_form)
    if year:
        data = data.filter(year=year)

    form = DirectionForm()
    return render(request, 'department/direction/all.html', {
        'data': data,
        'form': form,
    })


@login_required(login_url='login')
@security_decorator
def detail_direction(request: WSGIRequest, pk):
    object = get_object_or_404(Direction, pk=pk)


    create_group_form = SmallGroupForm()
    form = DirectionForm(instance=object)
    groups = SmallGroup.objects.filter(direction_id=object.id)
    return render(request, 'department/direction/detail.html', {
        'object': object,
        'data': groups,
        'form': form,
        'create_group_form': create_group_form,
    })



@security_decorator
@not_source_URL
def add_direction(request: WSGIRequest):
    form = DirectionForm(data=request.POST)
    if form.is_valid:
        form.save()
        messages.success(request, "Yangi yo'nalish qo'shildi")
    else:
        messages.error(request, """ Formani to'ldirishda xatolik yuz berdi """, extra_tags="danger")
    return redirect('d_all_direction')


@security_decorator
@not_source_URL
def delete_direction(request: WSGIRequest, pk):
    object = get_object_or_404(Direction, pk=pk)
    object.delete()
    return redirect('d_all_direction')



@security_decorator
@not_source_URL
def change_direction(request: WSGIRequest, pk):
    object = get_object_or_404(Direction, pk=pk)
    form = DirectionForm(data=request.POST, instance=object)
    if form.is_valid:
        form.save()
        messages.success(request, "Sozlamalar saqlandi")
    else:
        messages.error(request, "Formani to'ldirishda xatolik yuz berdi", extra_tags="danger")
    return redirect('d_detail_direction', pk=pk)


@security_decorator
@not_source_URL
def add_group_for_direction(request: WSGIRequest, pk):
    object = get_object_or_404(Direction, pk=pk)

    form = SmallGroupForm(data=request.POST)
    if form.is_valid:
        group = form.save(commit=False)
        group.direction = object
        group.save()
    return redirect('d_detail_direction', pk=pk)