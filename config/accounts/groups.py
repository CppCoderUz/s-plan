
from django.contrib.auth.models import Group

try:
    DEPARTMENT = Group.objects.get(name='department')
    FACULTY = Group.objects.get(name='faculty')
    CAFEDRA = Group.objects.get(name='cafedra')
    TEACHER = Group.objects.get(name='teacher')
    STUDENT = Group.objects.get(name='student')
except:
    raise NotImplementedError(
        """Group modelida ushbu obyektlardan biri mavjud emas. 
        department, faculty, cafedra, teacher, student"""
    )




