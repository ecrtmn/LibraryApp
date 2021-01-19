from django import forms
from .models import Order


class DateInput(forms.DateInput):
    input_type = 'date'


class OrderForm(forms.ModelForm):
    planned_end_at = forms.DateField(widget=DateInput)

    class Meta:
        model = Order
        fields = ['user', 'book', 'planned_end_at']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'book': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }


class OrderUpdateForm(forms.ModelForm):
    planned_end_at = forms.DateField(widget=DateInput)
    end_at = forms.DateField(widget=DateInput)

    class Meta:
        model = Order
        fields = ['planned_end_at', 'end_at']


class OrderOnClick(forms.ModelForm):
    planned_end_at = forms.DateField(widget=DateInput)

    class Meta:
        model = Order
        fields = ['planned_end_at']
