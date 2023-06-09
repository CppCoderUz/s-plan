from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.utils.translation import gettext_lazy as _

from accounts.models import (
    User,
    CafedraManager,
    DepartmentEmployee,
    FacultyManager,
)

@admin.register(User)
class _User(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone_number", "father_name", "image")}),
        (_("Permissions"),{"fields": ("is_active","is_staff","is_superuser","groups","user_permissions",),},),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ['username', 'last_name', 'first_name', 'father_name', 'email', 'phone_number', 'is_active', 'is_staff', 'is_superuser']

@admin.register(DepartmentEmployee)
class _DepartmentEmployee(admin.ModelAdmin):
    list_display = ['user', 'pk']

@admin.register(FacultyManager)
class _FacultyManager(admin.ModelAdmin):
    list_display = ['user', 'pk']

@admin.register(CafedraManager)
class _CafedraManager(admin.ModelAdmin):
    list_display = ['user', 'pk']








from curriculum.models import (
    Cafedra,
    Faculty,
    Science,
    Direction,
    SmallGroup,
    ScienceWithSemestr,
    Teacher,
    LessonWithTeacher,
    ProPractice,
    ProPracticeWithGroup,
)

@admin.register(Cafedra)
class _Cafedra(admin.ModelAdmin):
    list_display = ['name', 'manager', 'faculty']

@admin.register(Faculty)
class _Faculty(admin.ModelAdmin):
    list_display = ['name', 'manager']

@admin.register(Science)
class _Science(admin.ModelAdmin):
    list_display = ['name', 'cafedra']

@admin.register(Direction)
class _Direction(admin.ModelAdmin):
    list_display = ['name', 'max_semestr', 'faculty', 'code', 'language', 'study_form', 'year']

@admin.register(SmallGroup)
class _SmallGroup(admin.ModelAdmin):
    list_display = ['name', 'semestr', 'course', 'direction', 'sum_students']

@admin.register(ScienceWithSemestr)
class _ScienceWithSemestr(admin.ModelAdmin):
    list_display = ['science', 'science_code', 'exam', 'direction', 'semestr']

@admin.register(Teacher)
class _Teacher(admin.ModelAdmin):
    list_display = ['user', 'cafedra', 'pk']

@admin.register(LessonWithTeacher)
class _LessonWithTeacher(admin.ModelAdmin):
    list_display = ['science','group', 'lesson_type']

@admin.register(ProPractice)
class _ProPractice(admin.ModelAdmin):
    list_display = ['direction', 'semestr', 'time']

@admin.register(ProPracticeWithGroup)
class _ProPracticeWithGroup(admin.ModelAdmin):
    list_display = ['group', 'teacher', 'pro_practice']