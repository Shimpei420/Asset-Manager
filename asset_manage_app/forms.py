from django import forms

from asset_manage_app.models import housekeep
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class MakeRecord(forms.ModelForm):
    class Meta:
        model = housekeep
        fields = (
            "date",
            "category",
            "description",
            "amount"
        )

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

class SigninForm(AuthenticationForm):
    pass
