from django import template

register = template.Library()

def counter(number):
    return list(range(1, number+1))
register.filter(name='counter', filter_func=counter)


@register.filter('full_data')
def full_data(data):
    """ ScienseWithSemestr tipida queryset ma'lumot kelishi kk """
    _full_data = []

    for i in data:
        _full_data.append({
            'code': i.science_code,
            'science': i.science,
            'form': i.exam,
            'credit': i.credit,
            'hours': i.credit * 30,
            'lecture': ['' if i.lecture==0 else i.lecture][0],
            'practice': ['' if i.practice == 0 else i.practice][0],
            'seminar': ['' if i.seminar == 0 else i.seminar][0],
            'laboratory': ['' if i.laboratory == 0 else i.laboratory][0],
            'independent_work': ['' if i.independent_work == 0 else i.independent_work][0],
            'course_work': ['K' if i.course_work else ""][0],
            'pk': i.pk,
        })
    return _full_data