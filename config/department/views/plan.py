from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from curriculum.models import Direction, ScienceWithSemestr, Science
from department.decorators import not_source_URL, security_decorator
from department.forms import ScienceWithSemestrForm






@login_required(login_url='login')
@security_decorator
def plan_init(request: WSGIRequest, direction_id, semestr_id):
    direction = get_object_or_404(Direction, pk=direction_id)
    if direction.max_semestr < semestr_id:
        raise Http404("Ushbu semestr mavjud emas")
    data = ScienceWithSemestr.objects.filter(direction_id=direction_id, semestr=semestr_id)


    form = ScienceWithSemestrForm()
    return render(request, 'department/plan/init.html', {
        'direction': direction,
        'semestr_id': semestr_id,
        'data': data,
        'form': form,
    })



@security_decorator
@not_source_URL
def save_plan(request: WSGIRequest, direction_id, semestr_id, pk = None):
    if pk is not None:
        fs = f'_{pk}'
    else:
        fs = ''
    EXAM_TYPE = ("Imtihon", "Sinov")

    code = request.POST.get(f"code{fs}", None)
    science = request.POST.get(f"science{fs}", None)
    exam_type = request.POST.get(f"exam_type{fs}", None)
    credit = request.POST.get(f"credit{fs}", "")
    lecture = request.POST.get(f"lecture{fs}", "")
    practice = request.POST.get(f"practice{fs}", "")
    laboratory = request.POST.get(f"laboratory{fs}", "")
    seminar = request.POST.get(f"seminar{fs}", "")
    independent_work = request.POST.get(f"independent_work{fs}", "")
    course_work = request.POST.get(f"course_work{fs}", None)
    try:
        direction = Direction.objects.get(pk=direction_id)
        science = Science.objects.get(pk=science)
        if exam_type is None:
            raise
        if not (exam_type in EXAM_TYPE):
            raise
        course_work = True if course_work == "K" else False
        if pk is not None:
            object = ScienceWithSemestr.objects.get(pk=pk)
        else:
            object = ScienceWithSemestr()
        
        if credit == "":
            raise
        if lecture == "":
            lecture = 0
        if practice == "":
            practice = 0
        if laboratory == "":
            laboratory = 0
        if seminar == "":
            seminar = 0
        if independent_work == "":
            independent_work = 0

        object.credit = credit
        object.direction = direction
        object.semestr = semestr_id
        object.science_code = code
        object.science = science
        object.lecture = lecture
        object.practice = practice
        object.laboratory = laboratory
        object.seminar = seminar
        object.independent_work = independent_work
        object.exam = exam_type
        object.course_work = course_work
        object.save()
    except Exception as e:
        print(e)
        messages.error(request, "Formani to'ldirishda xatolik yuz berdi", extra_tags="danger")
    return redirect('d_plan_init', direction_id=direction_id, semestr_id=semestr_id)


@security_decorator
@not_source_URL
def delete_plan_row(request: WSGIRequest, pk):
    object = ScienceWithSemestr.objects.get(pk=pk)
    object.delete()
    direction_id = object.direction.pk
    semestr_id = object.semestr
    return redirect('d_plan_init', direction_id=direction_id, semestr_id=semestr_id)




@security_decorator
@not_source_URL
def get_sciense_list(request: WSGIRequest, direction_id, semestr_id):
    pk = request.POST.get("pk", None)

    try:
        direction = Direction.objects.get(pk=direction_id)
    except:
        return JsonResponse({})
    
    data_list = ScienceWithSemestr.objects.filter(direction_id=direction_id, semestr=semestr_id)
    pk_list = []
    for i in data_list:
        pk_list.append(i.science.pk)

    filter = request.POST.get('filter', None)
    if filter is not None:
        object_list = Science.objects.filter(name__contains=filter).all()
    else:
        object_list = Science.objects.all()
    
    empty_dict = {}
    empty_list = []

    for object in object_list:
        empty_list.append({'id': object.id, 'text': object.name, 'cafedra': object.cafedra.name})

    empty_dict['rezult'] = empty_list
    empty_dict["sum_objects"] = object_list.count()
    return JsonResponse(empty_dict)