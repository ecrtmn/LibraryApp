from django import forms
from .models import Author


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'id': 'name',
                                           'placeholder': 'Authors name'}),
            'surname': forms.TextInput(attrs={'class': 'form-control',
                                              'id': 'surname',
                                              'placeholder': 'Authors surname'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control',
                                                 'id': 'patronymic',
                                                 'placeholder': 'Authors patronymic'}),
            'bio': forms.TextInput(attrs={'class': 'form-control',
                                          'id': 'bio',
                                          'placeholder': 'Authors bio'}),
            'photo': forms.FileInput(attrs={'class': 'form-control',
                                            'id': 'file'}),
        }
