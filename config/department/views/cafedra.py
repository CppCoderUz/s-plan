from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages
from django.contrib.auth import hashers
from django.contrib.auth.decorators import login_required
from department.decorators import not_source_URL, security_decorator
from department.forms import UserForm, CafedraForm

from curriculum.models import Cafedra, CafedraManager, Teacher, Science, Faculty


@login_required(login_url='login')
@security_decorator
def all_cafedra(request: WSGIRequest):
    q = request.GET.get('q', False)
    if q:
        data = Cafedra.objects.filter(name__contains=q)
    else:
        data = Cafedra.objects.all()


    form = UserForm()
    cafedra_form = CafedraForm()
    return render(request, 'department/cafedra/all.html', {
        'search': True,
        'data': data,
        'form': form,
        'cafedra_form': cafedra_form,
    })

@login_required(login_url='login')
@security_decorator
def detail_cafedra(request: WSGIRequest, pk):
    object = get_object_or_404(Cafedra, pk=pk)
    science = Science.objects.filter(cafedra_id=pk).count()
    teachers = Teacher.objects.filter(cafedra_id=pk).count()
    data = Teacher.objects.filter(cafedra_id=pk)


    form = UserForm()    
    faculty_list = Faculty.objects.all()
    return render(request, 'department/cafedra/detail.html', {
        'object': object,
        'teachers': teachers,
        'science': science,
        'data': data,
        'form': form,
        'faculty_list': faculty_list,
    })



@security_decorator
@not_source_URL
def add_cafedra(request: WSGIRequest):
    user_form = UserForm(data=request.POST)
    cafedra_form = CafedraForm(data=request.POST)

    if user_form.is_valid and cafedra_form.is_valid:
        password = request.POST.get('password', False)
        password2 = request.POST.get('password2', False)
        if password != password2:
            pass
        else:
            user = user_form.save(commit=False)
            cafedra = cafedra_form.save(commit=False)
            user.password = hashers.make_password(password)
            user.save()
            manager = CafedraManager.objects.create(user=user)
            cafedra.manager = manager
            cafedra.save()
            return redirect('d_all_cafedra')
    else:
        pass
    messages.error(request, "Formani to'ldirishda xatolik", extra_tags="danger")
    return redirect('d_all_cafedra')



@security_decorator
@not_source_URL
def change_name_cafedra(request: WSGIRequest, pk):
    object = get_object_or_404(Cafedra, pk=pk)
    cafedra_name = request.POST.get('cafedra_name', False)
    if not cafedra_name:
        pass
    else:
        object.name = cafedra_name
        object.save()
    return redirect('d_detail_cafedra', pk=pk)


@security_decorator
@not_source_URL
def delete_cafedra(request: WSGIRequest, pk):
    object = get_object_or_404(Cafedra, pk=pk)
    object.manager.user.username = "deleted_account_%s" % str(object.manager.user.pk)
    object.manager.user.is_active = False
    object.manager.user.is_staff = False
    object.manager.user.save()
    object.manager.delete()
    object.delete()
    return redirect('d_all_cafedra')


@security_decorator
@not_source_URL
def change_manager_cafedra(request: WSGIRequest, pk):
    object = get_object_or_404(Cafedra, pk=pk)
    form = UserForm(data=request.POST)
    if form.is_valid:
        try:
            user = form.save(commit=False)
            user.password = hashers.make_password(user.password)
            user.save()
        except:
            messages.error(request, "Boshqa hodim ID kiriting", extra_tags="danger")
            return redirect('d_detail_cafedra', pk=pk)
        manager = CafedraManager.objects.create(user=user)
        old_manager = object.manager
        object.manager = manager
        object.save()
        messages.success(request, "Sozlamalar muvaffaqiyatli saqlandi")
        old_manager.user.username = "deleted_account_%s" % str(old_manager.user.pk)
        old_manager.user.is_active = False
        old_manager.user.is_staff = False
        old_manager.user.save()
        old_manager.delete()
        return redirect('d_detail_cafedra', pk=pk)
    else:
        messages.error(request, "Formani to'ldirishda xatolik bor", extra_tags="danger")
        return redirect('d_detail_cafedra', pk=pk)


@security_decorator
@not_source_URL
def change_faculty_cafedra(request: WSGIRequest, pk):
    object = get_object_or_404(Cafedra, pk=pk)
    try:
        faculty_id = int(request.POST.get('faculty_id', False))
        faculty = Faculty.objects.get(pk=faculty_id)
        object.faculty = faculty
        object.save()
        messages.success(request, "Sozlamalar saqlandi")
    except:
        messages.error(request, "Formani to'ldirishd xatolik yuz berdi", extra_tags="danger")
    return redirect('d_detail_cafedra', pk=pk)

# 