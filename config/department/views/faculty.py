from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages
from django.contrib.auth import hashers
from django.contrib.auth.decorators import login_required
from department.decorators import security_decorator, not_source_URL
from department.forms import ChangeFacultyManagerForm

from curriculum.models import (
    Faculty,
    FacultyManager,
    SmallGroup,
    Teacher,
    Cafedra,
    Science,
)


@login_required(login_url='login')
@security_decorator
def faculty_all(request: WSGIRequest):
    """ Barcha fakultetlar ro'yxati +filter +fakultet qo'shish """
    search = request.GET.get('q', None)
    if search:
        data = Faculty.objects.filter(name__contains=search)
    else:
        data = Faculty.objects.all()
    
    # add_faculty formasi
    form = ChangeFacultyManagerForm()
    return render(request, 'department/faculty/all.html', {
        'data': data,
        'search': True,
        'form': form,
    })



@login_required(login_url='login')
@security_decorator
def faculty_detail(request: WSGIRequest, pk):
    """ fakultet detail """
    object = get_object_or_404(Faculty, pk=pk)

    groups = SmallGroup.objects.filter(direction__faculty_id=pk)
    students = 0
    for i in groups:
        students += i.sum_students

    teachers = Teacher.objects.filter(cafedra__faculty_id=pk).count()

    cafedras = Cafedra.objects.filter(faculty_id=pk)
    data = []

    for i in cafedras:
        obj = dict()
        obj['teachers'] = Teacher.objects.filter(cafedra_id=i.pk).count()
        obj['science'] = Science.objects.filter(cafedra_id=i.pk).count()
        obj['name'] = i.name
        obj['manager'] = i.manager.user
        obj['object'] = i
        data.append(obj)

    change_moderator_form = ChangeFacultyManagerForm()

    return render(request, 'department/faculty/detail.html', {
        'object': object,
        'students': students,
        'teachers': teachers,
        'cafedras': cafedras.count(),
        'data': data,
        'form': change_moderator_form,
    })




@security_decorator
@not_source_URL
def change_faculty(request: WSGIRequest, pk):
    object = get_object_or_404(Faculty, pk=pk)
    name = request.POST.get('faculty_name', None)
    if name:
        object.name = name
        object.save()
    return redirect('d_faculty_detail', pk=pk)



@security_decorator
@not_source_URL
def delete_faculty(request: WSGIRequest, pk):
    object = get_object_or_404(Faculty, pk=pk)
    object.manager.user.username = "deleted_account_%s" % object.pk
    object.manager.user.is_active = False
    object.manager.user.is_staff = False
    object.manager.user.save()
    object.manager.delete()
    object.delete()
    return redirect('d_faculty_all')


@security_decorator
@not_source_URL
def change_manager(request: WSGIRequest, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    form = ChangeFacultyManagerForm(data=request.POST)

    if form.is_valid:
        password1 = form['password'].value()
        password2 = form['password2'].value()
        if not (password1 == password2):
            messages.error(request, """ Formani to'ldirishda xatolik """, extra_tags="danger")
            return redirect('d_faculty_detail', pk=pk)
        else:
            try:
                user = form.save()
                user.password = hashers.make_password(password1)
                user.save()

                manager = FacultyManager.objects.create(user=user)
                old_manager = faculty.manager
                old_user = old_manager.user
                old_manager.delete()
                # Eski user shunchaki bazada saqlanadigan bo'lib qoladi
                old_user.username = f"deleted_account_{old_user.pk}"
                old_user.is_active = False
                old_user.is_staff = False
                old_user.save()

                # Yangi manager tayinlandi
                faculty.manager = manager
                faculty.save()
                messages.success(request, """ Sozlamalar muvaffaqqiyatli saqlandi """)
            except Exception as e:
                print(e)
                messages.error(request, """ Kiritilgan Hodim ID avvaldan mavjud. Iltimos boshqa ID kiriting ! """, extra_tags='danger')
    else:
        messages.error(request, """ Formani to'ldirishda xatolik  yuz berdi """, extra_tags='danger')
    return redirect('d_faculty_detail', pk=pk)


@security_decorator
@not_source_URL
def add_faculty(request: WSGIRequest):
    form = ChangeFacultyManagerForm(data=request.POST)
    name = request.POST.get('faculty_name', False)
    if not name:
        messages.error(request, "Formani to'ldirishda xatolik yuz berdi", extra_tags="danger")
        return redirect('d_faculty_all')
    if form.is_valid:
        password1 = form['password'].value()
        password2 = form['password2'].value()
        if not (password1 == password2):
            return redirect('d_faculty_all')
        try:
            user = form.save(commit=False)
            user.password = hashers.make_password(password1)
            user.save()
            manager = FacultyManager.objects.create(user=user)
            Faculty.objects.create(manager=manager, name=name)
        except Exception as e: 
            print(e)
            messages.error(request, 'Ushbu hodim ID band. Boshqa ID kiriting')
            return redirect('d_faculty_all')
    else:
        messages.error(request, "Formani to'ldirishda xatolik yuz berdi", extra_tags="danger")
        return redirect('d_faculty_all')
    return redirect('d_faculty_all')