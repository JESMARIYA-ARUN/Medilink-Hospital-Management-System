# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from .models import CustomUser  # Import your custom user model

class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser  # <-- important
        fields = ["username", "email", "password1", "password2", "role"]  # role included

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name"] 
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }

class CustomProfileForm(UserChangeForm):
    password = None  # hide password field

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'phone', 'address', 'gender', 'dob',
            'specialization', 'hospital_contact'
        ]

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "gender": forms.Select(choices=[
                ("Male", "Male"),
                ("Female", "Female"),
                ("Other", "Other"),
            ], attrs={"class": "form-control"}),
            "dob": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "specialization": forms.TextInput(attrs={"class": "form-control"}),
            "hospital_contact": forms.TextInput(attrs={"class": "form-control"}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    # You can customize labels or widgets if you like
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



