from django import forms 

from accounts.models import User
from curriculum.models import Cafedra, Direction, SmallGroup, ScienceWithSemestr, Science




class ChangeFacultyManagerForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Parolni tasdiqlang")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Parolni kiriting')

    class Meta:
        model = User
        fields = [
            'username', 'password', 'password2', 'first_name', 'last_name', 'email', 
            'father_name', 'phone_number', 
        ]
    
    def __init__(self, *args, **kwargs):
        super(ChangeFacultyManagerForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.required = True
        self.fields['first_name'].label = 'Ism'
        self.fields['last_name'].label = 'Familya'
        self.fields['email'].label = 'E-mail manzili'
        self.fields['username'].label = 'Hodim ID'
        self.fields['father_name'].label = 'Otasining ismi'
        self.fields['phone_number'].label = 'Telefon raqami'
        self.fields['password'].label = 'Parol'


class UserForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Parolni tasdiqlang")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Parolni kiriting')

    class Meta:
        model = User
        fields = [
            'username', 'password', 'password2', 'first_name', 'last_name', 'email', 
            'father_name', 'phone_number', 
        ]
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.required = True
        self.fields['first_name'].label = 'Ism'
        self.fields['last_name'].label = 'Familya'
        self.fields['email'].label = 'E-mail manzili'
        self.fields['username'].label = 'Hodim ID'
        self.fields['father_name'].label = 'Otasining ismi'
        self.fields['phone_number'].label = 'Telefon raqami'
        self.fields['password'].label = 'Parol'

        
class CafedraForm(forms.ModelForm):

    class Meta:
        model = Cafedra
        fields = [
            'name', 'faculty'
        ]

    def __init__(self, *args, **kwargs):
        super(CafedraForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['faculty'].widget.attrs['class'] = 'form-select'
        self.fields['name'].label = 'Kafedra nomi'
        self.fields['faculty'].label = 'Fakulteti'



class DirectionForm(forms.ModelForm):
    class Meta:
        model = Direction
        fields = [
            'name', 'code', 'faculty', 'year',  
            'language', 'study_form'
        ]
    
    def __init__(self, *args, **kwargs):
        super(DirectionForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['year'].widget.attrs['class'] = 'form-control'
        self.fields['code'].widget.attrs['class'] = 'form-control'

        self.fields['faculty'].widget.attrs['class'] = 'form-select'
        self.fields['language'].widget.attrs['class'] = 'form-select'
        self.fields['study_form'].widget.attrs['class'] = 'form-select'



class SmallGroupForm(forms.ModelForm):
    class Meta:
        model = SmallGroup
        fields = [
            'number', 'code', 'sum_students'
        ]
    
    def __init__(self, *args, **kwargs):
        super(SmallGroupForm, self).__init__(*args, **kwargs)
        self.fields['number'].widget.attrs['class'] = 'form-control'
        self.fields['sum_students'].widget.attrs['class'] = 'form-control'
        self.fields['code'].widget.attrs['class'] = 'form-control'
        self.fields['sum_students'].label = 'Talabalar soni'
    
class SmallGroupFullForm(forms.ModelForm):
    class Meta:
        model = SmallGroup
        fields = [
            'number', 'code', 'sum_students', 'direction'
        ]
    
    def __init__(self, *args, **kwargs):
        super(SmallGroupFullForm, self).__init__(*args, **kwargs)
        self.fields['number'].widget.attrs['class'] = 'form-control'
        self.fields['sum_students'].widget.attrs['class'] = 'form-control'
        self.fields['code'].widget.attrs['class'] = 'form-control'
        self.fields['direction'].widget.attrs['class'] = 'form-select'

        self.fields['sum_students'].label = 'Talabalar soni'


class ScienceWithSemestrForm(forms.ModelForm):
    class Meta:
        model = ScienceWithSemestr
        fields = [
            'science_code', 'exam', 
            'credit', 'practice', 'lecture',
            'seminar', 'laboratory', 'independent_work',
        ]
    
    def __init__(self, *args, **kwargs):
        super(ScienceWithSemestrForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.required = True
        self.fields['exam'].widget.attrs['class'] = 'form-select'