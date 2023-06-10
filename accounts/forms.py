from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import User, UserProfile
from .validators import allow_only_images_validator


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']

    
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match"
            )
        

class UserProfileForm(forms.ModelForm):
    # NOTE: ImageField didn't support custom validator *
    # NOTE: FileField support custom validator images/docs and anything file upload

    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])

    # NOTE: CUSTOM ATTRIBUTS (Readonly)
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']

    # NOTE: CUSTOM ATTRIBUTS VERY USEFUL IN REAL LIFE (Readonly, etc)    
    # def __init__(self, *args, **kwargs):
    #     super(UserProfileForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         if field == 'latitude' or 'longitude':
    #             self.fields[field].widget.attrs['readonly'] = 'readonly'