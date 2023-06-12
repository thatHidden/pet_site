from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from axaxa.models import *
import datetime
import pytz


class AddLotForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = ['brand', 'model', 'generation', 'body', 'start_price', 'time_end', 'description', 'photo']

    def clean(self):
        data = self.cleaned_data
        if not AvailableCarList.objects.filter(brand=data.get('brand'),
                                               model=data.get('model'),
                                               generation=data.get('generation'),
                                               body=data.get('body')).exists():
            self.add_error('__all__', 'Car is not available for sale')
        if data.get('start_price') < 0:
            self.add_error('start_price', 'Price must be greater than or equal to 0')
        current_time = datetime.datetime.now(pytz.utc)
        end_time = data.get('time_end')
        min_end_time = current_time + datetime.timedelta(days=2)
        if end_time <= min_end_time:
            self.add_error('time_end', 'Time of the auction can not be less then 3 days')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddLotForm, self).form_valid(form)

    # def clean_brand(self):
    #     brand = self.cleaned_data.get('brand')
    #     if AvailableCarList.objects.filter(brand=brand).exists():
    #         return brand
    #     raise forms.ValidationError('Brand error')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Name')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password')
    password2 = forms.CharField(label='Repeat password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль')


class CommentForm(forms.ModelForm):
    # user = forms.ModelChoiceField(
    #     widget=forms.HiddenInput(),
    #     queryset=get_user_model().objects.all(),
    #     disabled=True  # запрещеает редактирование пользователем
    # )

    class Meta:
        model = Comment
        fields = ('content',)

    def clean(self):
        data = self.cleaned_data
        if data.get('content') is None:
            self.add_error('content', 'Empty comment')


    # def form_valid(self, form):  # хуйня вроде можно удалить
    #     form.instance.user = self.request.user
    #     return super(AddLotForm, self).form_valid(form)
