from django import forms
from .models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'phone', 'country')
        widgets = {
            'first_name':
            forms.TextInput(attrs={'placeholder': 'name'}),
            'email':
            forms.TextInput(attrs={'disabled': 'disabled'}),
            'last_name':
            forms.TextInput(attrs={'placeholder': 'last name'}),
            'phone':
            forms.TextInput(attrs={
                'placeholder': 'phone',
                'type': 'number'
            }),
        }


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('first_name', 'last_name', 'address_1', 'address_2', 'city',
                  'zip_code', 'state', 'phone')
        widgets = {
            'first_name':
            forms.TextInput(attrs={
                'required': "",
                'placeholder': 'your first name'
            }),
            'last_name':
            forms.TextInput(attrs={
                'required': "",
                'placeholder': 'your last name'
            }),
            'city':
            forms.TextInput(attrs={
                'required': "",
                'placeholder': '(ex):casablanca'
            }),
            'address_1':
            forms.TextInput(attrs={
                'required': "",
                'placeholder': 'address 1'
            }),
            'address_2':
            forms.TextInput(attrs={'placeholder': 'address 2 (optional)'}),
            'zip_code':
            forms.TextInput(
                attrs={
                    'required': "",
                    'placeholder': '(ex):46457',
                    'class': 'form-control'
                }),
            'state':
            forms.TextInput(
                attrs={
                    'required': "",
                    'placeholder': '(ex):rhamna',
                    'class': 'form-control'
                }),
            'phone':
            forms.TextInput(
                attrs={
                    'type': 'number',
                    'required': "",
                    'placeholder': '(ex):+1216789...',
                    'class': 'form-control'
                }),
        }
