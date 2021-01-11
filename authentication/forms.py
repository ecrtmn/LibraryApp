from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .models import CustomUser
from django import forms


class UserForm(forms.ModelForm):
    # password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Your password',
    #     'label': 'password'
    #     }))
    # password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Password confirm',
    #     'label': 'password confirmation'
    # }))
    class Meta:
        model = CustomUser
        fields = '__all__'
        exclude = ['is_active', 'updated_at', 'created_at', 'role', 'last_login', 'photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your password'}),
        }


class UserUpdate(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'id': 'first_name',
                                                 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'id': 'last_name',
                                                'placeholder': 'Last name'}),
            'photo': forms.FileInput(attrs={'class': 'form-control',
                                            'id': 'file'}),
        }


class UserPasswordChange(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'id': 'old_password',
                                                                     'placeholder': 'Old password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                      'id': 'new_password_1',
                                                                      'placeholder': 'New password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                      'id': 'new_password_2',
                                                                      'placeholder': 'New password(again)'}))

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']
