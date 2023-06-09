from django.db import models
from django.contrib.auth.models import AbstractUser


from accounts.groups import (
    DEPARTMENT,
    FACULTY,
    CAFEDRA,
    TEACHER,
    STUDENT
)


class User(AbstractUser):
    """ Asosiy foydlanuvchilar bazasi """
    phone_number = models.CharField(max_length=30, default='')
    father_name = models.CharField(max_length=100, default='')

    image = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name} ({self.username})'
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = '1. Userlar'



class DepartmentEmployee(models.Model):
    """ O'quv bo'limi xodimlari """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user)
    
    def save(self, *args, **kwargs):
        self.user.groups.add(DEPARTMENT)
        self.user.save()
        super(DepartmentEmployee, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.groups.remove(DEPARTMENT)
        self.user.save()
        super(DepartmentEmployee, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "O'quv bo'limi xodimi"
        verbose_name_plural = "2. O'quv bo'limi xodimlari"

    
class FacultyManager(models.Model):
    """ Dekanlar """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user)
    
    def save(self, *args, **kwargs):
        self.user.groups.add(FACULTY)
        self.user.save()
        super(FacultyManager, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.groups.remove(FACULTY)
        self.user.save()
        super(FacultyManager, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Dekan'
        verbose_name_plural = '3. Dekanlar'


class CafedraManager(models.Model):
    """ Kafedra mudiri """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user)
    
    def save(self, *args, **kwargs):
        self.user.groups.add(CAFEDRA)
        self.user.save()
        super(CafedraManager, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.user.groups.remove(CAFEDRA)
        self.user.save()
        super(CafedraManager, self).delete(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Mudir'
        verbose_name_plural = '4. Mudirlar'



