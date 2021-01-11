from django import forms
from .models import Order
from bootstrap_datepicker_plus import DatePickerInput


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'book', 'planned_end_at']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'book': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'planned_end_at': DatePickerInput(format='%Y-%m-%d'),
        }


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['planned_end_at', 'end_at']
        widgets = {
            'planned_end_at': DatePickerInput(format='%Y-%m-%d'),
            'end_at': DatePickerInput(format='%Y-%m-%d'),
        }