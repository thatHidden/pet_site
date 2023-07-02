import os

from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from axaxa.models import *
import datetime
import pytz


class SignupForm(SignupForm):
    """Extends base allauth sign up form"""
    first_name = forms.RegexField(max_length=10, regex=r'^[a-zA-Z]+$', label="Name", required=True, )

    class Meta:
        model = User
        field = ['first_name']


class UpdateUserPicture(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['photo']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_photo(self):
        current_names = CustomUser.objects.values_list('photo', flat=True)
        while True:
            random_string = get_random_string(length=10)
            if random_string not in current_names:
                self.cleaned_data['photo'].name = random_string + '.jpg'
                break
        if self.user.photo.name != "default":
            delete_path = self.user.photo.path
            os.remove(path=delete_path)
        return self.cleaned_data['photo']


class UpdateContactInfo(forms.ModelForm):
    first_name = forms.RegexField(max_length=10, regex=r'^[a-zA-Z]+$', label="Name", required=False)
    email = forms.EmailField(label="Email", required=False)
    phone_number = forms.CharField(max_length=15, required=False, label="Phone number")
    password = forms.PasswordInput()

    class Meta:
        model = CustomUser
        fields = ['first_name', 'email', 'phone_number', 'password']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        if data == '':
            return self.user.first_name
        return data

    def clean_email(self):
        data = self.cleaned_data.get('email')
        if data == '':
            return self.user.email
        return data

    def clean_phone_number(self):
        data = self.cleaned_data.get('phone_number')
        if data == '':
            return self.user.phone_number
        return data

    def clean(self):
        if check_password(self.cleaned_data.get('password'),
                          CustomUser.objects.get(username=self.user.username).password):
            return self.cleaned_data
        raise forms.ValidationError("Wrong password.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user


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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

    def clean(self):
        data = self.cleaned_data
        if data.get('content') is None:
            self.add_error('content', 'Empty comment')
