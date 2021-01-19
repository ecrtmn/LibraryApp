from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors', 'cover']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'id': 'name',
                                           'placeholder': 'Book title'}),
            'description': forms.TextInput(attrs={'class': 'form-control',
                                                  'id': 'description',
                                                  'placeholder': 'Book description'}),
            'count': forms.NumberInput(attrs={'class': 'form-control',
                                              'id': 'count',
                                              'placeholder': 'Book count',
                                              'min': 0}),
            'authors': forms.SelectMultiple(attrs={'multiple class': 'form-control',
                                                   'id': 'select'}),
            'cover': forms.FileInput(attrs={'class': 'form-control',
                                            'id': 'file'}),
        }
