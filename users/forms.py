from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Siswa'),
        ('instructor', 'Instruktur'),
    )
    
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'bio', 'phone_number', 'profile_picture')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mengatur label untuk field-field
        self.fields['first_name'].label = 'Nama Depan'
        self.fields['last_name'].label = 'Nama Belakang'
        self.fields['email'].label = 'Email'
        self.fields['bio'].label = 'Biografi'
        self.fields['phone_number'].label = 'Nomor Telepon'
        self.fields['profile_picture'].label = 'Foto Profil'