from django.db import models
from django.utils import timezone

from accounts.models import (
    CafedraManager,
    FacultyManager,
    User
)

from accounts.groups import TEACHER


class Faculty(models.Model):
    """ Fakultet """
    manager = models.OneToOneField(FacultyManager, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Fakultet'
        verbose_name_plural = '1. Fakultetlar'


class Cafedra(models.Model):
    """ Kafedra """
    manager = models.OneToOneField(CafedraManager, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Kafedra'
        verbose_name_plural = '2. Kafedralar'


class Science(models.Model):
    """ Fan """
    name = models.CharField(max_length=150)
    cafedra = models.ForeignKey(Cafedra, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name} ({str(self.cafedra)})'

    class Meta:
        verbose_name = 'Fan'
        verbose_name_plural = '3. Fanlar'




class Direction(models.Model):
    """ Yo'nalish """

    LANGUAGE_CHOICES = (
        ("O'zbek", "O'zbek"),
        ("Rus", "Rus"),
        ("Boshqa", "Boshqa")
    )

    STUDY_FORM_CHOICES = (
        ("Kunduzgi", "Kunduzgi"),
        ("Kechki", "Kechki"),
        ("Sirtqi", "Sirtqi"),
    )

    name = models.CharField(max_length=150, verbose_name='Yo\'nalish nomi')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name='Fakulteti')

    code = models.CharField(max_length=30,null=True, blank=True, verbose_name='Yo\'nalish kodi')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, verbose_name="Ta'lim tili")
    study_form = models.CharField(max_length=15,choices=STUDY_FORM_CHOICES, verbose_name="Ta'lim shakli")
    year = models.IntegerField(verbose_name='Qabul qilingan yili')

    @property
    def max_semestr(self):
        if self.study_form == "Kunduzgi":
            return 8
        elif self.study_form == "Kechki":
            return 9
        else:
            return 10

    def __str__(self) -> str:
        return f'{self.name} | {self.faculty} | {self.code}'

    class Meta:
        verbose_name = 'Yo\'nalish'
        verbose_name_plural = '4. Barcha yo\'nalishlar'





class SmallGroup(models.Model):
    """ Guruh """
    number = models.IntegerField(default=0, verbose_name="Guruh raqami")
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name="Yo'nalishi")
    code = models.CharField(max_length=50, verbose_name="Guruh kodi")
    sum_students = models.IntegerField(default=0)

    
    DONE = "O'qishni tamomlagan"
    
    @property
    def semestr(self):
        """ Semestri """
        month = timezone.now().month
        difference = timezone.now().year - self.direction.year
        _semestr = [2*difference+1 if month>=9 and month<=1 else 2*difference][0]
        if _semestr > self.direction.max_semestr:
            return SmallGroup.DONE
        return _semestr

    @property
    def course(self):
        """ Kursi """
        if self.semestr == SmallGroup.DONE:
            return SmallGroup.DONE
        return [self.semestr // 2 if self.semestr % 2 == 0 else self.semestr // 2 + 1][0]
        

    @property
    def name(self):
        """ Guruh nomi """
        if self.course == SmallGroup.DONE:
            return f'{1000 + self.number}'[1:] + f'-guruh ({[self.direction.year+4 if self.direction.max_semestr==8 else self.direction.year+4][0]}-bitiruvchilari)'
        return f'{self.course*100 + self.number} - guruh'
        


    def __str__(self) -> str:
        return f'{self.name} | {self.direction.name}'

    class Meta:
        verbose_name = 'Guruh'
        verbose_name_plural = '5. Guruhlar'


class ScienceWithSemestr(models.Model):
    """ Semestrda o'tiladigan fan """
    EXAM_TYPE = (
        ("Imtihon", "Imtihon"),
        ("Sinov", "Sinov"),
    )
    semestr = models.IntegerField(verbose_name="Semestr raqami")
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    science = models.ForeignKey(Science, on_delete=models.CASCADE)
    science_code = models.CharField(max_length=150, verbose_name="Fan kodi")
    exam = models.CharField(max_length=10, choices=EXAM_TYPE, verbose_name="Imtihon shakli")
    
    credit = models.IntegerField(default=0, verbose_name="Kredit miqdori")
    practice = models.IntegerField(default=0, verbose_name="Amaliyot")
    lecture = models.IntegerField(default=0, verbose_name="Ma'ruza")
    seminar = models.IntegerField(default=0, verbose_name="Seminar")
    laboratory = models.IntegerField(default=0, verbose_name="Labaratoriya")
    independent_work = models.IntegerField(default=0, verbose_name="Mustaqil ish")

    course_work = models.BooleanField(default=False, verbose_name="Kurs ishi")


    def __str__(self) -> str:
        return f'{self.science} | {self.semestr}-semestr | {self.direction}'
    
    class Meta:
        verbose_name = 'Fan rejasi'
        verbose_name_plural = '6. Semestrlik fanlar'


class Teacher(models.Model):
    """ O'qituvchi ( teacher ) """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cafedra = models.ForeignKey(Cafedra, on_delete=models.CASCADE, verbose_name="Kafedrasi")
    sciences = models.ManyToManyField(
        Science, 
        verbose_name="Fanlar", 
        related_name="sciences",
        related_query_name="sciences"
    )

    def __str__(self) -> str:
        return f'{self.user} ({self.cafedra})'
    
    def save(self, *args, **kwargs):
        self.user.groups.add(TEACHER)
        self.user.save()
        super(Teacher, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.groups.remove(TEACHER)
        self.user.save()
        super(Teacher, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "O'qituvchi"
        verbose_name_plural = "7. O'qituvchilar"



class LessonWithTeacher(models.Model):
    """ O'qituvchi uchun ajratilgan dars """
    LESSON_TYPE = (
        ("Amaliyot", "Amaliyot"),
        ("Ma'ruza", "Ma'ruza"),
        ("Seminar", "Seminar"),
        ("Labaratoriya", "Labaratoriya"),
        ("Mustaqil ta'lim", "Mustaqil ta'lim"),
        ("Kurs ishi", "Kurs ishi")
    )
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE, verbose_name="Dars turi")
    group = models.ForeignKey(SmallGroup, on_delete=models.CASCADE, verbose_name="Guruh")
    teacher = models.ManyToManyField(Teacher, blank=True, verbose_name="Dars beruvchi o'qituvchilar")
    science = models.ForeignKey(ScienceWithSemestr, on_delete=models.CASCADE, verbose_name="Fan")

    def __str__(self) -> str:
        return f'{self.lesson_type} | {self.group.name} | {self.science.science.name}'
    
    class Meta:
        verbose_name = 'Dars'
        verbose_name_plural = '8. Darslar'


class ProPractice(models.Model):
    time = models.IntegerField(verbose_name="Amaliyot muddati")
    semestr = models.IntegerField(verbose_name="Semestr")
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name="Yo'nalish")

    def __str__(self) -> str:
        return f'{self.direction} | {self.semestr}-semestr'
    
    class Meta:
        verbose_name = 'Malakaviy amaliyot reja'
        verbose_name_plural = '9. Malakaviy amaliyot rejalar'

class ProPracticeWithGroup(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, verbose_name="O'qituvchi")
    pro_practice = models.ForeignKey(ProPractice, on_delete=models.CASCADE)
    group = models.ForeignKey(SmallGroup, on_delete=models.CASCADE, verbose_name="Guruh")

    def __str__(self) -> str:
        return f'{self.pro_practice}'

    class Meta:
        verbose_name = 'Malakaviy amaliyot dars'
        verbose_name_plural = '10. Malakaviy amaliyot darslar'

