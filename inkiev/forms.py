from django import forms
from django.contrib.auth.models import User
from .models import PrivateEvent, Event, Place
import datetime


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    class Meta:
        model = User
        fields = ("username",)
        labels = {'username': 'Логин'}

    def clean(self):
        super(UserRegistrationForm, self).clean()
        errors = {}
        if self.cleaned_data.get('username') is None:
            errors['username'] = forms.ValidationError('Логин от 4 до 20 символов', code='len_login_error')
        elif len(self.cleaned_data.get('username')) < 4 or len(self.cleaned_data.get('username')) > 20:
            errors['username'] = forms.ValidationError('Логин от 4 до 20 символов', code='len_login_error')

        if self.cleaned_data.get('password1') is None:
            errors['password2'] = forms.ValidationError('Пароль от 6 символов', code='len_password_error')
        elif len(self.cleaned_data.get('password1')) < 6:
            errors['password2'] = forms.ValidationError('Пароль от 6 символов', code='len_password_error')

        if errors:
            raise forms.ValidationError(errors)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password2 != password1:
            raise forms.ValidationError(
                'Пароли не совпадают',
                code='password_mismatch',
            )
        return password2


class PrivateEventForm(forms.ModelForm):
    start_time = forms.DateTimeField(label='Дата начала', widget=forms.DateTimeInput, initial=datetime.datetime.now())

    class Meta:
        model = PrivateEvent
        fields = ('title', 'text', 'start_time')
        labels = {'title': 'Название', 'text': 'Описание', 'start_time': 'Дата и время  начала'}


class EventForm(forms.ModelForm):
    start_time = forms.DateTimeField(label='Дата начала', widget=forms.DateTimeInput, initial=datetime.datetime.now())

    class Meta:
        model = Event
        fields = ('title', 'text', 'start_time')
        labels = {'title': 'Название', 'text': 'Описание', 'start_time': 'Дата и время  начала'}


class PlaceForm(forms.ModelForm):

    class Meta:
        model = Place
        fields = ('title', 'text')
        labels = {'title': 'Название', 'text': 'Описание'}