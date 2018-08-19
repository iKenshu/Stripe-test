from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Customer, Subscription


class CustomerCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')


class SuscriptionForm(forms.ModelForm):
    """ Suscription Form """

    class Meta:
        model = Subscription
        fields = ('full_name', 'email')
